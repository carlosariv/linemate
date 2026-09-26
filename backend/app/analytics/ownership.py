import pandas as pd
import numpy as np

from app.models import Document, CrewMember, DocumentCategory

STALE_THRESHOLD_DAYS = 90
STALE_RISK_THRESHOLD_PCT = 50.0

def _documents_to_frame(documents: list[Document]) -> pd.DataFrame:
    return pd.DataFrame([
        {
            "id": document.id,
            "owner_id": document.owner_id,
            "days_since_reviewed": document.days_since_last_reviewed(),
            "stale_eligible": document.category != DocumentCategory.INCIDENT_REPORT
        }
        for document in documents
    ])

def _crew_members_to_frame(members: list[CrewMember]) -> pd.DataFrame:
    return pd.DataFrame([
        {
            "id": member.id,
            "station": member.station
        }
        for member in members
    ])

def compute_document_ownership(documents: list[Document], crew_members: list[CrewMember]) -> dict:
    document_df = _documents_to_frame(documents)
    member_df = _crew_members_to_frame(crew_members)

    merged = document_df.merge(
        member_df,
        left_on="owner_id",
        right_on="id",
        suffixes=("_document", "_member")
    )

    merged["is_stale"] = merged["stale_eligible"] & (merged["days_since_reviewed"] > STALE_THRESHOLD_DAYS)

    owned = merged.groupby("station").size()

    stale = merged.groupby("station")["is_stale"].sum().reindex(owned.index, fill_value=0)

    stations = owned.index.to_numpy()
    owned_array = owned.to_numpy(dtype=float)
    stale_array = stale.to_numpy(dtype=float)

    stale_share_pct = np.divide(
        stale_array, owned_array,
        out=np.zeros_like(stale_array),
        where=owned_array != 0,
    ) * 100

    flagged = stale_share_pct > STALE_RISK_THRESHOLD_PCT

    station_reports = [
        {
            "station": str(station.value),
            "owned_document_count": int(owned_array[i]),
            "stale_document_count": int(stale_array[i]),
            "stale_share_pct": float(stale_share_pct[i]),
            "is_stale_risk": bool(flagged[i])
        }
        for i, station in enumerate(stations)
    ]

    return {
        "stations": station_reports,
        "total_documents": int(len(documents))
    }