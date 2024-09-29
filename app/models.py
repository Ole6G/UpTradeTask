from pydantic import BaseModel, EmailStr, UUID4, Field
from typing import List, Optional


class ClientRequest(BaseModel):
    fio: str
    email: EmailStr
    uuid: UUID4
    report_name: str
    inn: str


class ReportBaseInfo(BaseModel):
    name: Optional[str] = None
    kpp: Optional[str] = None
    okpo: Optional[str] = None
    okato: Optional[str] = None
    okfs: Optional[str] = None
    okogu: Optional[str] = None
    okopf: Optional[str] = None
    opf: Optional[str] = None
    oktmo: Optional[str] = None
    registration_date: Optional[str] = None


class ReportContactInfo(BaseModel):
    phones: Optional[List[str]] = []
    websites: Optional[List[str]] = []


class ReportProcurementInfo(BaseModel):
    total_sum: Optional[float] = None
    total_count: Optional[int] = None


class ReportTaxInfo(BaseModel):
    year: int
    value: float


class ReportDetailedTaxInfo(BaseModel):
    total: float
    details: Optional[List[ReportTaxInfo]] = []


class ClientReport(BaseModel):
    fio: str
    email: str
    uuid: UUID4
    report_name: str
    base_info: ReportBaseInfo
    contact_info: ReportContactInfo
    procurement_info: ReportProcurementInfo
    tax_info: ReportDetailedTaxInfo
