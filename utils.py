from langgraph.graph import MessagesState

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import convert_to_messages

import functools

import tools


def get_tokens(response):
    """
    Extracts token usage information from the response.
    """
    if not response or "messages" not in response:
        return 0, 0, 0
    
    total_tokens = 0
    prompt_tokens = 0
    completion_tokens = 0  
    
    for message in response["messages"]:
        if message.response_metadata and "token_usage" in message.response_metadata:
            total_tokens += message.response_metadata["token_usage"]["total_tokens"]
            prompt_tokens += message.response_metadata["token_usage"]["prompt_tokens"]
            completion_tokens += message.response_metadata["token_usage"]["completion_tokens"]
    
    return {"total_tokens": total_tokens,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens}


def rename(newname):
    def decorator(f):
        f.__name__ = newname
        return f
    return decorator

def make_specialist(plant, llm):
    blooming = functools.partial(tools.get_bloom_data_whole, plant=plant)

    @rename(f"get_bloom_data_{plant}")
    def get_bloom_data(year: int):
        """
        Get bloom data for the specified plant and year.

        Args:
            year (int): The year for which to retrieve bloom data.

        Returns:
            dict: A dictionary containing bloom data and additional information.
        """
        return blooming(year = year)
    
    specialist_agent = create_react_agent(
        model=llm,
        tools=[get_bloom_data],
        prompt=(
            f'Du bist ein Assistent, der Informationen über die Blütezeit von der Pflanze {plant} bereitstellt. Nutze get_bloom_data_whole mit {plant} als ersten parameter, um Informationen über die Blütezeit von {plant} zu erhalten.'
            'Antworte auf die Fragen in folgendme Format: Antworte in JSON und folge dem Schema: { "type": "object", "properties": { "response": { "type": "boolean" }, "reasoning": { "type": "string" } }, "required": [ "response", "reasoning" ] }'
            'response soll auf true gesetzt werden, wenn die Pflanze blüht und false, wenn sie nicht blüht.'
        ),
        name=f"{plant}_agent",
    )
    return specialist_agent



def pretty_print_message(message, indent=False):
    pretty_message = message.pretty_repr(html=True)
    if not indent:
        print(pretty_message)
        return

    indented = "\n".join("\t" + c for c in pretty_message.split("\n"))
    print(indented)


def pretty_print_messages(update, last_message=False):
    is_subgraph = False
    if isinstance(update, tuple):
        ns, update = update
        # skip parent graph updates in the printouts
        if len(ns) == 0:
            return

        graph_id = ns[-1].split(":")[0]
        print(f"Update from subgraph {graph_id}:")
        print("\n")
        is_subgraph = True

    for node_name, node_update in update.items():
        update_label = f"Update from node {node_name}:"
        if is_subgraph:
            update_label = "\t" + update_label

        print(update_label)
        print("\n")

        messages = convert_to_messages(node_update["messages"])
        if last_message:
            messages = messages[-1:]

        for m in messages:
            pretty_print_message(m, indent=is_subgraph)
        print("\n")