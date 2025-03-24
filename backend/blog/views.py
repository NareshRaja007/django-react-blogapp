from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import *
from rest_framework.permissions import IsAuthenticated
from blog.authentication import CustomJWTAuthentication 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.pagination import PageNumberPagination



class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            user_id = data.get('user_id')
            name = data.get('name')
            contact_number = data.get('contact_number')
            password = data.get('password')

            if not all([user_id, name, contact_number, password]):
                logger.warning("User registration failed: Missing fields")
                payload = Common.create_payload(False, "Mandatory fields missing", "Fields not filled", None)
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"User {name} registered successfully")
                payload = Common.create_payload(True, "User registered successfully", None, None)
                return Response(payload, status=status.HTTP_201_CREATED)
            else:
                logger.warning(f"User registration validation failed: {serializer.errors}")
                payload = Common.create_payload(False, "Validation failed", serializer.errors, None)
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error in user registration: {str(e)}", exc_info=True)
            payload = Common.create_payload(False, "Internal server error", str(e), None)
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            user_id = data.get('user_id')
            password = data.get('password')

            if not all([user_id, password]):
                logger.warning("User login failed: Missing credentials")
                payload = Common.create_payload(False, "Missing credentials", "ID or password not provided", None)
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            user = UserDetails.objects.filter(user_id=user_id).first()
            if user and check_password(password, user.password):
                tokens = RefreshToken.for_user(user)
                response_data = {
                    "refresh": str(tokens),
                    "access": str(tokens.access_token),
                    "user": {
                        "id": user.user_id,
                        "name": user.name,
                        "contact_number": user.contact_number,
                    }
                }
                logger.info(f"User {user.name} logged in successfully")
                payload = Common.create_payload(True, "Login successful", None, response_data)
                return Response(payload, status=status.HTTP_200_OK)

            logger.warning("User login failed: Invalid credentials")
            payload = Common.create_payload(False, "Invalid credentials", "Incorrect ID or password", None)
            return Response(payload, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            logger.error(f"Error in user login: {str(e)}", exc_info=True)
            payload = Common.create_payload(False, "Internal server error", str(e), None)
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            users = UserDetails.objects.all()
            serializer = UserRegisterSerializer(users, many=True)
            logger.info("Fetched user list successfully")
            payload = Common.create_payload(True, "User list retrieved", None, serializer.data)
            return Response(payload, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching user list: {str(e)}", exc_info=True)
            payload = Common.create_payload(False, "Internal server error", str(e), None)
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ViewAllPosts(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            posts = BlogPost.objects.all().order_by('-created_at')
            records_per_page = int(request.GET.get('records_per_page', 10))
            page = request.GET.get('page', 1)

            paginator = Paginator(posts, records_per_page)
            try:
                paginated_posts = paginator.page(page)
            except PageNotAnInteger:
                paginated_posts = paginator.page(1)
            except EmptyPage:
                paginated_posts = []

            serializer = BlogPostSerializer(paginated_posts, many=True)
            pagination = {
                "total_pages": paginator.num_pages,
                "current_page": paginated_posts.number if paginated_posts else 1,
                "records_per_page": records_per_page,
                "total_records": paginator.count
            }

            payload = Common.create_payload(True, "Blog posts fetched successfully", None, {"pagination": pagination, "data": serializer.data})
            return Response(payload, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching blog posts: {str(e)}")
            payload = Common.create_payload(False, "Error fetching blog posts", str(e), None)
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlogPostCreateView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        try:
            auth_result = CustomJWTAuthentication().authenticate(request)
            if not auth_result:
                payload = Common.create_payload(False, "Authentication failed", None, None)
                return Response(payload, status=status.HTTP_401_UNAUTHORIZED)

            user, token = auth_result

            posts = BlogPost.objects.filter(user=user)
            serializer = BlogPostSerializer(posts, many=True)
            payload = Common.create_payload(True, "Blog posts fetched successfully", None, serializer.data)
            return Response(payload, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching blog posts: {str(e)}")
            payload = Common.create_payload(False, "Error fetching blog posts", str(e), None)
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            auth_result = CustomJWTAuthentication().authenticate(request)
            if not auth_result:
                payload = Common.create_payload(False, "Authentication failed", None, None)
                return Response(payload, status=status.HTTP_401_UNAUTHORIZED)

            user, token = auth_result

            data = request.data.copy()
            data['created_by'] = user.name  

            blog_post = BlogPost(user=user, **data)
            blog_post.save()

            serializer = BlogPostSerializer(blog_post)
            payload = Common.create_payload(True, "Blog post created successfully", None, serializer.data)
            return Response(payload, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating blog post: {str(e)}", exc_info=True)
            payload = Common.create_payload(False, "Error creating blog post", str(e), None)
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request):
        try:
            post_id = request.data.get('post_id')
            if not post_id:
                payload = Common.create_payload(False,"Post Id is manadatory to edit","Post Id is manadatory to edit",None)
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            auth_result = CustomJWTAuthentication().authenticate(request)
            if not auth_result:
                return Response(Common.create_payload(False, "Authentication failed", None, None), status=status.HTTP_401_UNAUTHORIZED)

            user, token = auth_result
            blog_post = BlogPost.objects.filter(id=post_id, user=user).first()
            if not blog_post:
                return Response(Common.create_payload(False, "Blog post not found or unauthorized", None, None), status=status.HTTP_404_NOT_FOUND)

            serializer = BlogPostSerializer(blog_post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(Common.create_payload(True, "Blog post updated successfully", None, serializer.data), status=status.HTTP_200_OK)
            return Response(Common.create_payload(False, "Validation error", serializer.errors, None), status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Error updating blog post: {str(e)}", exc_info=True)
            return Response(Common.create_payload(False, "Error updating blog post", str(e), None), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            post_id = request.query_params.get('post_id')
            if not post_id:
                payload = Common.create_payload(False,"Post Id is manadatory to edit","Post Id is manadatory to edit",None)
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            auth_result = CustomJWTAuthentication().authenticate(request)
            if not auth_result:
                payload = Common.create_payload(False, "Authentication failed", None, None)
                return Response(payload, status=status.HTTP_401_UNAUTHORIZED)

            user, token = auth_result
            blog_post = BlogPost.objects.filter(id=post_id, user=user).first()
            if not blog_post:
                payload = Common.create_payload(False, "Blog post not found or unauthorized", None, None)
                return Response(payload, status=status.HTTP_404_NOT_FOUND)

            blog_post.delete()
            payload = Common.create_payload(True, "Blog post deleted successfully", None, None)
            return Response(payload, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error deleting blog post: {str(e)}", exc_info=True)
            payload = Common.create_payload(False, "Error deleting blog post", str(e), None)
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
