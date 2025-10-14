from fastapi import APIRouter, Depends
from app.schemas.notification_schema import NotificationCreate, NotificationResponse
from app.controllers.notification_controller import create_notification, get_notifications_for_user, mark_notification_as_read
from app.auth import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/", response_model=NotificationResponse)
def send_notification(
    notif: NotificationCreate,
    current_user: str = Depends(get_current_user)
):
    return create_notification(
        sender_id=current_user,
        receiver_id=notif.receiver_id,
        message=notif.message,
        notif_type=notif.type,
        target_id=notif.target_id,
        target_type=notif.target_type
    )

@router.get("/", response_model=list[NotificationResponse])
def get_user_notifications(current_user: str = Depends(get_current_user)):
    return get_notifications_for_user(current_user)

@router.put("/{notification_id}/read")
def mark_as_read(notification_id: str):
    return mark_notification_as_read(notification_id)
