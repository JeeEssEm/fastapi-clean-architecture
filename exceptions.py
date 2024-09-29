from starlette import status
from fastapi import HTTPException

NewsNotFound = HTTPException(status.HTTP_404_NOT_FOUND, 'News not found')
CommentNotFound = HTTPException(status.HTTP_404_NOT_FOUND, 'Comment not found')
NewsAccessDenied = HTTPException(status.HTTP_403_FORBIDDEN, 'You do not have permission to edit these news')
CommentAccessDenied = HTTPException(status.HTTP_403_FORBIDDEN, 'You do not have permission to edit this comment')
