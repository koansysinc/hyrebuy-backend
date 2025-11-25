"""
Groups API
Days 29-35: Group Buying Backend (Phase 2)

CRUD operations for buying groups with invite system
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, date
import string
import random
from uuid import UUID

from app.database import get_db
from app.models.buying_group import BuyingGroup
from app.models.group_member import GroupMember
from app.models.group_invite import GroupInvite
from app.models.group_message import GroupMessage
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter(prefix="/groups", tags=["Groups"])


# Utility function to generate unique invite codes
def generate_invite_code(length: int = 8) -> str:
    """Generate a random invite code"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


# Schemas

class CreateGroupRequest(BaseModel):
    """Request to create a new buying group"""
    name: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    target_location: str = Field(..., min_length=1)
    target_configuration: Optional[str] = None
    budget_min: Optional[int] = None
    budget_max: int
    minimum_members: int = Field(default=5, ge=2)
    maximum_members: int = Field(default=20, le=100)
    close_by_date: Optional[date] = None


class UpdateGroupRequest(BaseModel):
    """Request to update a group"""
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    target_location: Optional[str] = None
    target_configuration: Optional[str] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    minimum_members: Optional[int] = Field(None, ge=2)
    maximum_members: Optional[int] = Field(None, le=100)
    status: Optional[str] = None


class GroupResponse(BaseModel):
    """Group data response"""
    id: str
    admin_id: str
    name: str
    description: Optional[str]
    target_location: str
    target_configuration: Optional[str]
    budget_min: Optional[int]
    budget_max: int
    minimum_members: str
    maximum_members: str
    close_by_date: Optional[date]
    status: str
    current_member_count: str
    committed_member_count: str
    expected_discount_percent: Optional[str]
    current_discount_tier: Optional[str]
    invite_code: str
    is_discoverable: str
    created_at: datetime

    @field_validator('close_by_date', mode='before')
    @classmethod
    def convert_datetime_to_date(cls, v):
        if v is not None and isinstance(v, datetime):
            return v.date()
        return v


class JoinGroupRequest(BaseModel):
    """Request to join a group via invite code"""
    invite_code: str


class CreateInviteRequest(BaseModel):
    """Request to create a group invite"""
    sharing_method: Optional[str] = "link"  # whatsapp, email, link


class InviteResponse(BaseModel):
    """Invite data response"""
    id: str
    group_id: str
    invite_code: str
    status: str
    sharing_method: Optional[str]
    created_at: datetime
    whatsapp_link: Optional[str] = None


class SendMessageRequest(BaseModel):
    """Request to send a message to a group"""
    message: str = Field(..., min_length=1, max_length=5000)
    message_type: str = Field(default="text")


class MessageResponse(BaseModel):
    """Message data response"""
    id: str
    group_id: str
    sender_id: str
    message: str
    message_type: str
    is_pinned: str
    created_at: datetime


# API Endpoints

@router.post("", response_model=GroupResponse)
async def create_group(
    request: CreateGroupRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new buying group

    Phase 2: Group Buying Feature
    Creates a group with the current user as admin
    Requires Authentication: Yes (Bearer token)
    """
    try:
        # Generate unique invite code
        invite_code = generate_invite_code()

        # Ensure invite code is unique
        while True:
            existing = await db.execute(
                select(BuyingGroup).where(BuyingGroup.invite_code == invite_code)
            )
            if not existing.scalar_one_or_none():
                break
            invite_code = generate_invite_code()

        # Create group
        new_group = BuyingGroup(
            admin_id=current_user.id,
            name=request.name,
            description=request.description,
            target_location=request.target_location,
            target_configuration=request.target_configuration,
            budget_min=request.budget_min,
            budget_max=request.budget_max,
            minimum_members=str(request.minimum_members),
            maximum_members=str(request.maximum_members),
            close_by_date=request.close_by_date,
            invite_code=invite_code,
            status="forming",
            current_member_count="1",  # Admin is first member
        )

        db.add(new_group)
        await db.flush()  # Get the group ID

        # Add admin as first member
        admin_member = GroupMember(
            group_id=new_group.id,
            user_id=current_user.id,
            status="committed",
            joined_at=datetime.utcnow(),
            committed_at=datetime.utcnow(),
        )
        db.add(admin_member)

        await db.commit()
        await db.refresh(new_group)

        return GroupResponse(
            id=str(new_group.id),
            admin_id=str(new_group.admin_id),
            name=new_group.name,
            description=new_group.description,
            target_location=new_group.target_location,
            target_configuration=new_group.target_configuration,
            budget_min=new_group.budget_min,
            budget_max=new_group.budget_max,
            minimum_members=new_group.minimum_members,
            maximum_members=new_group.maximum_members,
            close_by_date=new_group.close_by_date,
            status=new_group.status,
            current_member_count=new_group.current_member_count,
            committed_member_count=new_group.committed_member_count,
            expected_discount_percent=new_group.expected_discount_percent,
            current_discount_tier=new_group.current_discount_tier,
            invite_code=new_group.invite_code,
            is_discoverable=new_group.is_discoverable,
            created_at=new_group.created_at,
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create group: {str(e)}")


@router.get("", response_model=List[GroupResponse])
async def list_groups(
    status: Optional[str] = Query(None, description="Filter by status"),
    location: Optional[str] = Query(None, description="Filter by location"),
    configuration: Optional[str] = Query(None, description="Filter by configuration"),
    discoverable_only: bool = Query(True, description="Show only discoverable groups"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    List buying groups with filters

    Phase 2: Group Buying Feature
    Allows users to browse available groups
    """
    try:
        # Build query
        query = select(BuyingGroup)

        # Apply filters
        if discoverable_only:
            query = query.where(BuyingGroup.is_discoverable == "true")

        if status:
            query = query.where(BuyingGroup.status == status)

        if location:
            query = query.where(BuyingGroup.target_location.ilike(f"%{location}%"))

        if configuration:
            query = query.where(BuyingGroup.target_configuration == configuration)

        # Order by created date
        query = query.order_by(BuyingGroup.created_at.desc())

        # Pagination
        query = query.offset((page - 1) * limit).limit(limit)

        result = await db.execute(query)
        groups = result.scalars().all()

        return [
            GroupResponse(
                id=str(g.id),
                admin_id=str(g.admin_id),
                name=g.name,
                description=g.description,
                target_location=g.target_location,
                target_configuration=g.target_configuration,
                budget_min=g.budget_min,
                budget_max=g.budget_max,
                minimum_members=g.minimum_members,
                maximum_members=g.maximum_members,
                close_by_date=g.close_by_date,
                status=g.status,
                current_member_count=g.current_member_count,
                committed_member_count=g.committed_member_count,
                expected_discount_percent=g.expected_discount_percent,
                current_discount_tier=g.current_discount_tier,
                invite_code=g.invite_code,
                is_discoverable=g.is_discoverable,
                created_at=g.created_at,
            )
            for g in groups
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list groups: {str(e)}")


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific group by ID"""
    try:
        query = select(BuyingGroup).where(BuyingGroup.id == UUID(group_id))
        result = await db.execute(query)
        group = result.scalar_one_or_none()

        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        return GroupResponse(
            id=str(group.id),
            admin_id=str(group.admin_id),
            name=group.name,
            description=group.description,
            target_location=group.target_location,
            target_configuration=group.target_configuration,
            budget_min=group.budget_min,
            budget_max=group.budget_max,
            minimum_members=group.minimum_members,
            maximum_members=group.maximum_members,
            close_by_date=group.close_by_date,
            status=group.status,
            current_member_count=group.current_member_count,
            committed_member_count=group.committed_member_count,
            expected_discount_percent=group.expected_discount_percent,
            current_discount_tier=group.current_discount_tier,
            invite_code=group.invite_code,
            is_discoverable=group.is_discoverable,
            created_at=group.created_at,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get group: {str(e)}")


@router.post("/{group_id}/join")
async def join_group(
    group_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Join a group

    Phase 2: Group Buying Feature
    Adds current user to the group
    Requires Authentication: Yes (Bearer token)
    """
    try:
        # Get group
        group_query = select(BuyingGroup).where(BuyingGroup.id == UUID(group_id))
        result = await db.execute(group_query)
        group = result.scalar_one_or_none()

        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        current_user_id = str(current_user.id)

        # Check if group is full
        current_count = int(group.current_member_count)
        max_count = int(group.maximum_members)
        if current_count >= max_count:
            raise HTTPException(status_code=400, detail="Group is full")

        # Add member
        new_member = GroupMember(
            group_id=UUID(group_id),
            user_id=UUID(current_user_id),
            status="interested",
            joined_at=datetime.utcnow(),
        )
        db.add(new_member)

        # Update group member count
        group.current_member_count = str(current_count + 1)

        await db.commit()

        return {"message": "Successfully joined group", "group_id": group_id}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to join group: {str(e)}")


@router.post("/{group_id}/invites", response_model=InviteResponse)
async def create_invite(
    group_id: str,
    request: CreateInviteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create an invite link for a group

    Phase 2: Group Buying - Viral Loop
    Generates shareable invite codes
    Requires Authentication: Yes (Bearer token)
    """
    try:
        # Get group
        group_query = select(BuyingGroup).where(BuyingGroup.id == UUID(group_id))
        result = await db.execute(group_query)
        group = result.scalar_one_or_none()

        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        # Generate unique invite code
        invite_code = generate_invite_code(10)
        while True:
            existing = await db.execute(
                select(GroupInvite).where(GroupInvite.invite_code == invite_code)
            )
            if not existing.scalar_one_or_none():
                break
            invite_code = generate_invite_code(10)

        # Create invite
        new_invite = GroupInvite(
            group_id=UUID(group_id),
            inviter_id=current_user.id,
            invite_code=invite_code,
            sharing_method=request.sharing_method,
            status="pending",
        )

        db.add(new_invite)
        await db.commit()
        await db.refresh(new_invite)

        # Generate WhatsApp link if sharing via WhatsApp
        whatsapp_link = None
        if request.sharing_method == "whatsapp":
            invite_url = f"https://hyrebuy.com/groups/join/{invite_code}"
            message = f"Join my property buying group '{group.name}' on HyreBuy! We're looking for {group.target_configuration} in {group.target_location}. {invite_url}"
            whatsapp_link = f"https://wa.me/?text={message.replace(' ', '%20')}"

        return InviteResponse(
            id=str(new_invite.id),
            group_id=str(new_invite.group_id),
            invite_code=new_invite.invite_code,
            status=new_invite.status,
            sharing_method=new_invite.sharing_method,
            created_at=new_invite.created_at,
            whatsapp_link=whatsapp_link,
        )

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create invite: {str(e)}")


@router.post("/join/{invite_code}")
async def join_via_invite(
    invite_code: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Join a group using an invite code

    Phase 2: Group Buying - Viral Loop
    Allows new users to join via shared links
    Requires Authentication: Yes (Bearer token)
    """
    try:
        # Find invite
        invite_query = select(GroupInvite).where(GroupInvite.invite_code == invite_code)
        result = await db.execute(invite_query)
        invite = result.scalar_one_or_none()

        if not invite:
            raise HTTPException(status_code=404, detail="Invalid invite code")

        if invite.status != "pending":
            raise HTTPException(status_code=400, detail="Invite already used or expired")

        # Get group
        group_query = select(BuyingGroup).where(BuyingGroup.id == invite.group_id)
        result = await db.execute(group_query)
        group = result.scalar_one_or_none()

        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        # Check if already a member
        member_query = select(GroupMember).where(
            and_(
                GroupMember.group_id == invite.group_id,
                GroupMember.user_id == current_user.id
            )
        )
        existing = await db.execute(member_query)
        if existing.scalar_one_or_none():
            return {"message": "Already a member", "group_id": str(group.id)}

        # Add member
        new_member = GroupMember(
            group_id=invite.group_id,
            user_id=current_user.id,
            status="interested",
            invited_by=invite.inviter_id,
            invited_at=invite.created_at,
            joined_at=datetime.utcnow(),
        )
        db.add(new_member)

        # Update group member count
        current_count = int(group.current_member_count)
        group.current_member_count = str(current_count + 1)

        # Mark invite as accepted
        invite.status = "accepted"
        invite.accepted_at = datetime.utcnow()
        invite.invitee_id = UUID(current_user_id)

        await db.commit()

        return {
            "message": "Successfully joined group",
            "group_id": str(group.id),
            "group_name": group.name
        }

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to join via invite: {str(e)}")


@router.get("/{group_id}/messages", response_model=List[MessageResponse])
async def get_group_messages(
    group_id: str,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """Get messages for a group"""
    try:
        query = (
            select(GroupMessage)
            .where(GroupMessage.group_id == UUID(group_id))
            .order_by(GroupMessage.created_at.desc())
            .limit(limit)
        )

        result = await db.execute(query)
        messages = result.scalars().all()

        return [
            MessageResponse(
                id=str(m.id),
                group_id=str(m.group_id),
                sender_id=str(m.sender_id),
                message=m.message,
                message_type=m.message_type,
                is_pinned=m.is_pinned,
                created_at=m.created_at,
            )
            for m in reversed(messages)  # Reverse to show oldest first
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get messages: {str(e)}")


@router.post("/{group_id}/messages", response_model=MessageResponse)
async def send_message(
    group_id: str,
    request: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Send a message to a group

    Requires Authentication: Yes (Bearer token)
    """
    try:
        # Verify user is a member
        member_query = select(GroupMember).where(
            and_(
                GroupMember.group_id == UUID(group_id),
                GroupMember.user_id == current_user.id
            )
        )
        result = await db.execute(member_query)
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Not a member of this group")

        # Create message
        new_message = GroupMessage(
            group_id=UUID(group_id),
            sender_id=current_user.id,
            message=request.message,
            message_type=request.message_type,
        )

        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)

        return MessageResponse(
            id=str(new_message.id),
            group_id=str(new_message.group_id),
            sender_id=str(new_message.sender_id),
            message=new_message.message,
            message_type=new_message.message_type,
            is_pinned=new_message.is_pinned,
            created_at=new_message.created_at,
        )

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")
