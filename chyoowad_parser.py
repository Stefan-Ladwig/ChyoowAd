import re, json, copy, time

#input_file = "template_canvas.txt"
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
    stream = open("template_modified.excalidraw", encoding="utf-8")
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


def tree_to_json(tree):
    elements_template = get_template_json()
    elements = dict()
    elements_buffer = dict()
    current_elements = list()

    for id, node in tree.node_dict.items():
        current_elements = copy.deepcopy(elements_template)
        for element in current_elements:
            match(element["id"]):
                case "oberes_emoji":
                    element["text"] = node.choice_up
                case "unteres_emoji":
                    element["text"] = node.choice_down
                case "mittleres_emoji":
                    element["text"] = node.state
                case "emoji_klein":
                    element["text"] = node.origin

            #if "text" in element.keys() and "fontSize" in element.keys():
                #element["fontSize"] = float(element["fontSize"]) / len(element["text"])**(1/2)

            if "text" in element.keys() and "originalText" in element.keys():
                element["originalText"] = element["text"]

            element["id"] = str(node.counter) + "_" + element["id"]
            element["x"] += node.counter * 3000

            elements_buffer = elements_buffer | {element["id"]: element}
        elements = elements | {id: elements_buffer}
        elements_buffer = dict()

    for id, node in tree.node_dict.items():
        parent = node
        if not node.choice_up in tree.node_dict:
            continue
            
        top_child = tree.node_dict[parent.choice_up]

        elements[parent.origin][str(parent.counter)+"_oberes_emoji"]["link"] = \
            "https://excalidraw.com/?element=" + str(top_child.counter) + "_mittleres_emoji"
        
        elements[top_child.origin][str(top_child.counter)+"_emoji_klein"]["link"] = \
            "https://excalidraw.com/?element=" + str(parent.counter) + "_mittleres_emoji"

        if not node.choice_down in tree.node_dict:
            continue

        bot_child = tree.node_dict[parent.choice_down]

        elements[parent.origin][str(parent.counter)+"_unteres_emoji"]["link"] = \
            "https://excalidraw.com/?element=" + str(bot_child.counter) + "_mittleres_emoji"
        
        elements[bot_child.origin][str(bot_child.counter)+"_emoji_klein"]["link"] = \
            "https://excalidraw.com/?element=" + str(parent.counter) + "_mittleres_emoji"

    elements_list = list()        
    for element in elements.values():
        for nudel in element.values():
            elements_list.append(nudel)

    stream = open("template_modified.excalidraw", encoding="utf-8")
    outer_json = json.load(stream)
    stream.close()
    outer_json["elements"] = elements_list
    time_stamp = str(round(time.time()))
    output = open(time_stamp+"_new_test_modified.excalidraw", "x")
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
    print("end programm")