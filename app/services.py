import httpx
from fastapi import HTTPException

from app.config import API_BASE_URL, API_KEY
from app.models import ClientRequest, ClientReport, ReportBaseInfo, ReportContactInfo, ReportProcurementInfo, \
    ReportDetailedTaxInfo, ReportTaxInfo


async def fetch_data_from_api(endpoint: str, params: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}{endpoint}", params=params)
        return response.json()


async def generate_report(request: ClientRequest) -> ClientReport:
    try:
        base_info = await fetch_data_from_api("/api3/req", {"inn": request.inn, "key": API_KEY})
        taxes_info = await fetch_data_from_api("/api3/taxes", {"inn": request.inn, "key": API_KEY})
        procurement_info = await fetch_data_from_api("/api3/govPurchasesOfCustomer",
                                                     {"inn": request.inn, "key": API_KEY})

        # Fill base info
        base = ReportBaseInfo(
            name=base_info["name"],
            kpp=base_info.get("kpp"),
            okpo=base_info.get("okpo"),
            okato=base_info.get("okato"),
            okfs=base_info.get("okfs"),
            okogu=base_info.get("okogu"),
            okopf=base_info.get("okopf"),
            opf=base_info.get("opf"),
            oktmo=base_info.get("oktmo"),
            registration_date=base_info.get("registrationDate")
        )

        # Fill contact info
        contact = ReportContactInfo(
            phones=base_info.get("phones", []),
            websites=base_info.get("websites", [])
        )

        # Fill procurement info
        procurement = ReportProcurementInfo(
            total_sum=sum(item["sum"] for item in procurement_info.get("items", [])),
            total_count=len(procurement_info.get("items", []))
        )

        # Fill tax info
        taxes_list = [ReportTaxInfo(year=year, value=taxes_info[year]) for year in taxes_info]
        taxes_total = sum(item.value for item in taxes_list)
        taxes = ReportDetailedTaxInfo(total=taxes_total, details=taxes_list)

        report = ClientReport(
            fio=request.fio,
            email=request.email,
            uuid=request.uuid,
            report_name=request.report_name,
            base_info=base,
            contact_info=contact,
            procurement_info=procurement,
            tax_info=taxes
        )

        return report

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 403:
            return None  # Здесь возвращаем None, который потом обрабатываем как 403
        if exc.response.status_code == 400:
            raise HTTPException(status_code=422, detail=exc.response.json())
        raise HTTPException(status_code=500, detail=str(exc))