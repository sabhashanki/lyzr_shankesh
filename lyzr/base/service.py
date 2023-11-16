import logging
from typing import Optional, Union

from llama_index import ServiceContext
from llama_index.callbacks import CallbackManager
from llama_index.embeddings.utils import EmbedType
from llama_index.llms.utils import LLMType
from llama_index.prompts import PromptTemplate
from llama_index.prompts.base import BasePromptTemplate
from llama_index.node_parser.simple import SimpleNodeParser

from lyzr.utils.llm_utils import set_default_prompt_template

logger = logging.getLogger(__name__)


class LyzrService:
    @staticmethod
    def from_defaults(
        llm: Optional[LLMType] = "default",
        embed_model: Optional[EmbedType] = "default",
        system_prompt: str = None,
        query_wrapper_prompt: Union[str, BasePromptTemplate] = None,
        **kwargs,
    ) -> ServiceContext:
        if not system_prompt and not query_wrapper_prompt:
            system_prompt, query_wrapper_prompt = set_default_prompt_template()
        if isinstance(query_wrapper_prompt, str):
            query_wrapper_prompt = PromptTemplate(template=query_wrapper_prompt)

        callback_manager: CallbackManager = kwargs.get(
            "callback_manager", CallbackManager()
        )

        node_parser = SimpleNodeParser.from_defaults(
            chunk_size=512,
            chunk_overlap=10,
            callback_manager=callback_manager,
        )

        service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
            system_prompt=system_prompt,
            query_wrapper_prompt=query_wrapper_prompt,
            callback_manager=callback_manager,
            node_parser=node_parser,
            **kwargs,
        )

        return service_context
