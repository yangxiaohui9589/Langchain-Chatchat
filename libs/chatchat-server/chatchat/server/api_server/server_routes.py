from typing import Literal

from fastapi import APIRouter, Body

from chatchat.server.types.server.response.base import BaseResponse
from chatchat.settings import Settings
from chatchat.server.utils import get_prompt_template, get_server_configs, get_server_settings

server_router = APIRouter(prefix="/server", tags=["Server State"])

available_template_types = list(Settings.prompt_settings.model_fields.keys())

# 服务器相关接口
server_router.post(
    "/configs",
    summary="获取服务器原始配置信息",
)(get_server_configs)


@server_router.post("/get_prompt_template", summary="获取服务区配置的 prompt 模板", response_model=BaseResponse)
def get_server_prompt_template(
        type: str = Body(
            "llm_model", description="模板类型，可选值：{available_template_types}"
        ),
        name: str = Body("default", description="模板名称"),
):
    prompt_template = get_prompt_template(type=type, name=name)
    if prompt_template is None:
        return BaseResponse.error("Prompt template not found")
    return BaseResponse.success(prompt_template)

@server_router.get("/get_server_settings", summary="获取Yaml配置信息", response_model=BaseResponse)
def get_chatchat_server_settings():
    basic_settings = get_server_settings()
    if basic_settings is None:
        return BaseResponse.error("Yaml settings not found")
    return BaseResponse.success(basic_settings)
