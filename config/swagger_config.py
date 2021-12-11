from drf_yasg import openapi

# https://drf-yasg.readthedocs.io/en/stable/drf_yasg.html?highlight=type_#module-drf_yasg.openapi


class AuthSwaggerSchema:
    post_signup_manual_parameters = [
        openapi.Parameter(
            "email",
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            required=True,
            default="abcde@gmail.com",
            description="email",
        ),
        openapi.Parameter(
            "password",
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            required=True,
            default="qwerasdf",
            description="password",
        ),
    ]

    post_signup_responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: success)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: user signed up)",
                ),
            },
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: error)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: user already exists)",
                ),
            },
        ),
        500: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: error)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: internal server error)",
                ),
            },
        ),
    }

    post_signin_request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        require=["email", "password"],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                require=True,
                default="abcde@gmail.com",
                description="email",
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING,
                require=True,
                default="qwerasdf",
                description="password",
            ),
        },
    )

    post_signin_responses = {
        200: openapi.Response(
            description="sigin success",
            examples={
                "application/json": {
                    "status": "success",
                    "message": "user signed in",
                    "access_token": "access token",
                }
            },
        ),
        400: openapi.Response(
            description="sigin success",
            examples={
                "application/json": {
                    "status": "error",
                    "message": "password is invalid",
                }
            },
        ),
        500: openapi.Response(
            description="sigin success",
            examples={
                "application/json": {"status": "error", "message": "error message"}
            },
        ),
    }

    get_users_responses = {200: "success", 500: "internal server error"}

    patch_password_request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        require=["current_password", "new_password"],
        properties={
            "current_password": openapi.Schema(
                type=openapi.TYPE_STRING,
                require=True,
                default="qwerasdf",
                description="current password",
            ),
            "new_password": openapi.Schema(
                type=openapi.TYPE_STRING,
                require=True,
                default="qwerasdf1",
                description="new password",
            ),
        },
    )

    patch_password_responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: success)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: changed password)",
                ),
            },
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: error)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: user does not exist, password is invalid, password is same",
                ),
            },
        ),
        500: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: error)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: internal server error)",
                ),
            },
        ),
    }

    delete_signout_request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        require=["password"],
        properties={
            "password": openapi.Schema(
                type=openapi.TYPE_STRING,
                require=True,
                default="qwerasdf",
                description="password",
            )
        },
    )

    delete_signout_responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: success)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: user signed out)",
                ),
            },
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: error)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: user does not exist, password is invalid",
                ),
            },
        ),
        500: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: error)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: internal server error)",
                ),
            },
        ),
    }


class BoardSwaggerSchema:
    get_posts_responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: success)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: found all posts)",
                ),
                "data": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_NUMBER),
                            "author": openapi.Schema(type=openapi.TYPE_STRING),
                            "title": openapi.Schema(type=openapi.TYPE_STRING),
                            "content": openapi.Schema(type=openapi.TYPE_STRING),
                            "created_at": openapi.Schema(type=openapi.TYPE_STRING),
                            "updated_at": openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                ),
            },
        ),
        500: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: error)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: internal server error)",
                ),
            },
        ),
    }

    delete_posts_responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: success)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: deleted all posts)",
                ),
            },
        ),
        500: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: error)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: internal server error)",
                ),
            },
        ),
    }

    get_posts_path_manual_parameters = [
        openapi.Parameter(
            "post_id",
            openapi.IN_PATH,
            type=openapi.TYPE_NUMBER,
            required=True,
            default="10",
            description="post id",
        )
    ]

    get_posts_path_responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: success)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: found all posts)",
                ),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "author": openapi.Schema(type=openapi.TYPE_STRING),
                        "title": openapi.Schema(type=openapi.TYPE_STRING),
                        "content": openapi.Schema(type=openapi.TYPE_STRING),
                        "created_at": openapi.Schema(type=openapi.TYPE_STRING),
                        "updated_at": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            },
        ),
        500: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: error)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: internal server error)",
                ),
            },
        ),
    }

    patch_posts_path_responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: success)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING, description="message (e.g: edited post)"
                ),
            },
        ),
        500: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: error)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: internal server error)",
                ),
            },
        ),
    }

    put_posts_path_responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: success)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING, description="message (e.g: edited post)"
                ),
            },
        ),
        500: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: error)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: internal server error)",
                ),
            },
        ),
    }

    delete_posts_path_responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: success)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING, description="message (e.g: deleted post)"
                ),
            },
        ),
        500: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING, description="status (e.g: error)"
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="message (e.g: internal server error)",
                ),
            },
        ),
    }
