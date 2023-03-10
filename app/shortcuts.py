from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app import config

settings = config.get_settings()
templates = Jinja2Templates(directory=settings.templates_dir)


def render(
    request, template_name, context={}, status_code: int = 200, cookies: dict = {}
):
    ctx = context.copy()
    ctx.update({"request": request})
    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str, status_code=status_code)
    # print(request.cookies)
    response.set_cookie(key="darkmode", value=1)
    if len(cookies) > 0:
        # set HTTPonly cookies
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True)
    # delete cookies
    # for key in request.cookies.keys():
    #     response.delete_cookie(key=key)

    return response
