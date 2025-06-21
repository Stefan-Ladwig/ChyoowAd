import re, json, copy, time

input_file = "parse_test.txt"


class Node():
    def __init__(self, origin, state, choice_up, choice_down):
        self.origin = origin
        self.state = state
        self.choice_up = choice_up
        self.choice_down = choice_down
        self.previous_choice = None
        self.counter = None

    def save_counter(self, counter):
        self.counter = counter

    def save_previous_choice(self, up_or_down):
        self.previous_choice = up_or_down



class Tree():

    def __init__(self):
        self.node_counter = 0
        self.node_dict = dict()

    def _add_node(self, new_node):
        new_node.save_counter(self.node_counter)
        self.node_dict[new_node.origin] = new_node
        self.node_counter += 1
    
    def add_node_from_str(self, string):
        new_node = string_to_node(string)
        self._add_node(new_node)



def extract_node_parts(string):
    node_parts = list()
    string = string.replace(" ", "")
    node_parts = string.split(",")

    assert(len(node_parts) == 4)
    
    return node_parts


def get_template_json():
    stream = open("template.excalidraw", encoding="utf-8")
    outer_json = json.load(stream)
    stream.close()
    return outer_json["elements"]


def shift_elements(elements):
    for element in elements:
        element["x"] += 1000
    return elements


def parse_input(stream):
    new_tree = origin_tree()
    for line in stream.readlines():
        new_tree.add_node_from_str(line.strip())
    return new_tree


def add_link_to_elements(elements, origin_node, origin_element, target_node, target_element):
    origin_element_id = str(origin_node.counter) + origin_element
    target_element_id = str(target_node.counter) + target_element
    link_url = "https://excalidraw.com/?element=" + target_element_id
    elements[origin_node.origin][origin_element_id]["link"] = link_url


def link_parent_with_children(parent_node, node_dict, elements):

    for child in ({"id": parent_node.choice_up, "element": "_oberes_emoji"},
                  {"id": parent_node.choice_down, "element": "_unteres_emoji"}):

        if not child["id"] in node_dict:
            continue
        
        child_node = node_dict[child["id"]]
        add_link_to_elements(elements, parent_node, child["element"], child_node, "_mittleres_emoji")
        add_link_to_elements(elements, child_node, "_emoji_klein", parent_node, "_mittleres_emoji")


def link_all_parents_and_children(node_dict, elements):
   
    for node in node_dict.values():
        link_parent_with_children(
            parent_node=node,
            node_dict=node_dict,
            elements=elements
        )


def generate_elements_from_node(elements_template, node):
    element_node_dict = {
        "oberes_emoji": node.choice_up,
        "unteres_emoji": node.choice_down,
        "mittleres_emoji": node.state,
        "emoji_klein": node.origin
    }
    generated_elements = dict()

    for element in elements_template:
        if element["id"] in element_node_dict:
            element["text"] = element_node_dict[ element["id"] ]

        if "text" in element.keys() and "originalText" in element.keys():
            element["originalText"] = element["text"]

        element["id"] = str(node.counter) + "_" + element["id"]
        element["x"] += node.counter * 3000

        generated_elements = generated_elements | {element["id"]: element}

    return generated_elements


def get_elements_from_nodes(node_dict, json_elements_template):
    elements = dict()
    elements_template = list()

    for id, node in node_dict.items():
        elements_template = copy.deepcopy(json_elements_template)
        node_elements = generate_elements_from_node(elements_template, node)
        elements = elements | {id: node_elements}

    return elements
    

def tree_to_json(tree):

    elements = get_elements_from_nodes(tree.node_dict, get_template_json())
    
    link_all_parents_and_children(tree.node_dict, elements)

    elements_list = list()        
    for element in elements.values():
        for nudel in element.values():
            elements_list.append(nudel)

    stream = open("template.excalidraw", encoding="utf-8")
    outer_json = json.load(stream)
    stream.close()
    outer_json["elements"] = elements_list
    time_stamp = str(round(time.time()))
    output = open("generated/" + time_stamp + "_new_test.excalidraw", "x")
    json.dump(outer_json, output)
    output.close()


def origin_tree():
    origin = "👣"
    state = "👋"
    choice_up = "ℹ️"
    choice_down = "🆗"
    new_node = Node(origin, state, choice_up, choice_down)
    new_tree = Tree()
    new_tree._add_node(new_node)
    return new_tree


def string_to_node(string):
    node_parts = extract_node_parts(string)
    node = Node(*node_parts)
    return node


if __name__ == "__main__":
    stream = open(input_file, encoding="utf-8")
    tt = parse_input(stream)
    tree_to_json(tt)
    stream.close()
    print("Programm finished!")