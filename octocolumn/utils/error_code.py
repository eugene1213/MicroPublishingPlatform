def kr_error_code(x):
    return {
        401: {
            "title": "Sign in Failed",
            "message": "아이디와 비밀번호를 확인해 주세요"
        },
        402: {
            "title": "Sign in Failed",
            "message": "올바르지 않은 사용자 입니다"
        },
        403: {
            "title": "Profile Error",
            "message": "프로필은 반드시 입력해야합니다."

        },
        405: {
            "title": "No activation yet",
            "message": "인증되지 않은 작가 계정입니다",
        },
        406: {
            "title": "Unauthorized Email",
            "message": "이메일 인증이 완료되지 않은 계정입니다.",
        },
        407: {
            "title": "Not purchased",
            "message": "구매하지 않은 칼럼입니다.",
        },
        408: {
            "title": "Already registered",
            "message": "이미 등록 되었습니다.",

        },
        409: {
            "title": "Already registered",
            "message": "이미 포스팅 되었거나 존재하지 않는 칼럼입니다.",
        },
        410: {
            "title": "Upload Failed",
            "message": "이미지 업로드에 실패하였습니다",

        },
        411: {
            "title": "Lack of quantity",
            "message": "분량이 부족합니다",
        },
        412: {
            "title": "No cover",
            "message": "커버 이미지가 없습니다"
        },
        413: {
            "title": "Tag error",
            "message": "태그가 1개이상 5개이하로 설정해야 합니다.",

        },
        414: {
            "title": "Not enough point",
            "message": "포인트가 부족합니다",
        },
        415: {
            "title": "Already register",
            "message": "이미 신청된 칼럼이 있습니다",
        },
        416: {
            "title": "Buy failed",
            "message": "구매에 실패 하셨습니다",

        },
        417: {
            "title": "Save failed",
            "message": "저장 가능한 글은 10개 입니다.",
        },
        422: {
            "title": "Reply failed",
            "message": "댓글 등록에 실패하셨습니다",
        },
        423: {
            "title": "Deleted Reply",
            "message": "삭제된 댓글 입니다",

        },
        424: {
            "title": "Invalid request",
            "message": "올바르지 않은 요청값입니다.",
        },
        431: {
            "title": "Already rated",
            "message": "이미 평가한 칼럼입니다.",
        },
        432: {
            "title": "Already exists this email",
            "message": "이미 가입 되어있는 이메일 입니다.",
        },
        433: {
            "title": "This account does not have an email address.",
            "message": "이 계정에는 이메일이 등록되어있지 않습니다.",
        },

        500: {
            "title": "Fatal error",
            "message": "허용되지 않은 접속입니다.",
        },
    }.get(x, "No data")