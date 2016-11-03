from models import *
from pprint import pprint
import pydotplus
import re


def find_my_module(my_module, my_payment_methods_list, recursion=0):
    MAX_DEPTH=5
    module_list = [my_module, ]
    display_merchant = False

    pprint(my_module.name)
    my_recursion = recursion + 1

    if my_recursion < MAX_DEPTH:
        for my_dependency in ModuleWritesToModule.objects.all().filter(from_module=my_module):
            if my_payment_methods_list is None \
                    or len(my_dependency.payment_methods.values()) is 0 \
                    or len(set(my_payment_methods_list).intersection(set(my_dependency.payment_methods.iterator()))) > 0:
                list_of_dependencies, customer_facing = find_my_module(my_dependency.to_module, my_payment_methods_list, my_recursion)
                module_list = list(set(module_list) | set(list_of_dependencies))
                # pprint("%s %s %s" % (my_module, my_dependency.access_direction, my_dependency.to_module))
                if customer_facing:
                    display_merchant = True

    # if my_recursion == 1:
    #     for my_dependency in ModuleWritesToModule.objects.all().filter(to_module=my_module).filter(access_direction=READ):
    #         if my_payment_methods_list is None \
    #                 or len(my_dependency.payment_methods.values()) is 0 \
    #                 or len(set(my_payment_methods_list).intersection(set(my_dependency.payment_methods.iterator()))) > 0:
    #             module_list.append(my_dependency.from_module)
    #             # pprint("%s %s %s" % (my_module, my_dependency.access_direction, my_dependency.to_module))
    #             if my_dependency.from_module.customer_facing:
    #                 display_merchant = True

    return module_list, display_merchant


def module(my_module_name, my_payment_methods_list=None):
    #
    # Compile a list of modules to include in this graph
    #

    ARROW_SIZE = 0.7
    FONT_SIZE = 8

    if my_module_name is not None:
        my_module = Module.objects.get(slug=my_module_name)
        if my_payment_methods_list is not None:
            my_payment_method_list = []
            for payment_method in my_payment_methods_list:
                my_payment_method_list.append(PaymentMethod.objects.get(slug=payment_method))
        else:
            my_payment_method_list = None

        list_of_modules, display_merchant = find_my_module(my_module, my_payment_method_list)
    else:
        list_of_modules = set(Module.objects.all())
        my_payment_method_list = None
    #
    # Build the graph
    #
    if my_module_name is not None:
        graph_name = my_module.name
    else:
        graph_name = 'Module Overview'
    graph = pydotplus.Dot(graph_type='digraph', graph_name=graph_name, strict=True)
    graph.set('smoothing', 'graph_dist')
    #graph.set_prog('neato')
    graph.set('overlap', 'false')
    if my_module_name is None:
        graph.set('rankdir', 'LR')
        graph.set('splines',  True)
        graph.set('ratio', 0.45)
    else:
        graph.set('ratio', 0.55)
        graph.set('splines', 'ortho')
    #graph.set('splines', True)

    graph.set('newrank', True)
    graph.set('concentrate', True)
    graph.set('pad', 0.5)
    graph.set('nodesep', 0.1)
    graph.set('ranksep', 0.4)
    graph.set('stylesheet', '/static/PaymentFont/css/paymentfont.css')
    graph.set('imagepath', '/home/tbartel/Projekte/ServiceCatalog')

    if my_module_name is None or my_module.customer_facing:
        node = pydotplus.Node()
        node.set_name('Merchant')
        node.set('fontsize', FONT_SIZE)
        node.set('fontname', 'PaymentFont,sans-serif')
        node.set('fillcolor', 'cornflowerblue')
        node.set('style', 'filled')
        if my_module_name is None:
            node.set('shape', 'cds')
        else:
            node.set('shape', 'invhouse')
        graph.add_node(node)
        if my_module_name is not None:
            edge = pydotplus.Edge('Merchant:s', my_module.__unicode__())
            edge.set('arrowsize', ARROW_SIZE)
            graph.add_edge(edge)

    for one_node in list_of_modules:
        node = pydotplus.Node()
        node.set_name(one_node.__unicode__())
        if len(one_node.__unicode__()) > 10:
            split_point = one_node.__unicode__().rfind(' ')
            my_label = one_node.__unicode__()[:split_point] + "\n" + one_node.__unicode__()[split_point+1:]
            node.set('label', my_label)

        if one_node.is_service:
            node.set('shape', 'octagon')
        else:
            node.set('shape', 'box')

        if one_node.is_external:
            node.set('fillcolor', 'lightgreen')
            node.set('style', 'filled')

        node.set('URL', '/module/%s/' % one_node.slug)

        node.set('fontsize', FONT_SIZE)
        node.set('fontname', 'PaymentFont,sans-serif')
        if my_module_name is not None and one_node is my_module:
            node.set('shape', 'box3d    ')
            node.set('style', 'filled')
            node.set('fillcolor', 'gold')
        graph.add_node(node)


        for dependency in ModuleWritesToModule.objects.all().filter(from_module=one_node).iterator():
            label = ''
            if dependency.to_module in list_of_modules:
                if my_payment_method_list is None or len(dependency.payment_methods.values()) == 0:
                    # pprint("a: %s" % dependency.payment_methods )
                    edge = pydotplus.Edge(dependency.from_module.__unicode__(), dependency.to_module.__unicode__())
                    edge.set('arrowsize', ARROW_SIZE)
                    edge.set('fontsize', FONT_SIZE)
                    edge.set('fontname', 'PaymentFont,sans-serif')
                    if dependency.comment is not None:
                        edge.set('xlabel', dependency.comment)

                    if dependency.access_direction == READ:
                        edge.set('dir', 'back')
                    elif dependency.access_direction == BOTH:
                        edge.set('dir', 'both')
                else:
                    filtered_paynment_methd = list(set(dependency.payment_methods.iterator()) & set(my_payment_method_list))
                    if len(filtered_paynment_methd) > 0:
                        edge = pydotplus.Edge(dependency.from_module.__unicode__(), dependency.to_module.__unicode__())
                        edge.set('fontname', 'PaymentFont,sans-serif')
                        edge.set('fontsize', FONT_SIZE)
                        edge.set('arrowsize', ARROW_SIZE)


                        for depending_paynment_method in filtered_paynment_methd:
                            pprint("%s" % depending_paynment_method.name)
                            # edge = pydotplus.Edge(dependency.from_module.__unicode__(), dependency.to_module.__unicode__())
                            if depending_paynment_method in my_payment_method_list:
                                if depending_paynment_method.image is not None:
                                    label += "%s" % depending_paynment_method.image
                                else:
                                    label += "%s" % depending_paynment_method

                            if dependency.access_direction == READ:
                                edge.set('dir', 'back')
                            elif dependency.access_direction == BOTH:
                                edge.set('dir', 'both')
                        if dependency.comment:
                            if len(label) > 0:
                                label += "\n(%s)" % dependency.comment
                            else:
                                label = "%s" % (dependency.comment, )

                        edge.set('xlabel', label)

                if dependency.is_online:
                    edge.set('color', 'red')
                elif dependency.is_online is False:
                    edge.set('color', 'blue')

                graph.add_edge(edge)
            if my_module_name is None and dependency.from_module.customer_facing:
                edge = pydotplus.Edge('Merchant', dependency.from_module.__unicode__())
                edge.set('arrowsize', ARROW_SIZE)
                graph.add_edge(edge)

    #
    # Workaround to make SVG responsive
    #
    my_graph = graph.create(format='svg', )
    my_graph = re.sub(r"( width=)", " min-width=", my_graph )
    my_graph = re.sub(r"( height=)", " min-height=", my_graph )

    return my_graph


def instance(instance_name):
    #
    # Compile a list of all hardware and instances to include in this graph
    #

    my_hardware_nodes = {}
    my_instance_nodes = []
    add_the_internet = False

    my_hardware = Hardware.objects.all()
    my_hardware = my_hardware.filter(instance__slug=instance_name)

    my_instance = Instance.objects.get(slug=instance_name)

    for one in my_hardware:
        if not one.type in my_hardware_nodes:
            my_hardware_nodes[one.type] = []
        if one not in my_hardware_nodes[one.type]:
            my_hardware_nodes[one.type].append(one)

        for dependency in one.hardware_on_hardware.iterator():
            if not dependency.type in my_hardware_nodes:
                my_hardware_nodes[dependency.type] = []
            if dependency not in my_hardware_nodes[dependency.type]:
                my_hardware_nodes[dependency.type].append(dependency)

        for dependency in one.depending_on_instance.iterator():
            if dependency not in my_instance_nodes:
                my_instance_nodes.append(dependency)
                if dependency.customer_accesable:
                    add_the_internet = True

    #
    # Build the graph
    #
    graph = pydotplus.Dot(graph_type='digraph')
    graph.set_prog('dot')
    # graph.set('mode', 'hier')
    graph.set('splines', 'polyline')
    graph.set('remincross', 'true')
    graph.set('overlap', 'false')

    graph.set('newrank', True)

    if add_the_internet:
        node = pydotplus.Node()
        node.set_name('Merchant')
        node.set('shape', 'box3d')
        graph.add_node(node)

    for hardware_type in my_hardware_nodes:
        if hardware_type != Hardware.LB:
            subgraph = pydotplus.Cluster(graph_name=hardware_type)
            subgraph.set('rank', 'same')
        for to_hardware in my_hardware_nodes[hardware_type]:
            node = pydotplus.Node()
            node.set_name(to_hardware.name)
            node.set('shape', 'box')
            if hardware_type != Hardware.LB:
                subgraph.add_node(node)
            else:
                graph.add_node(node)

            for from_hardware in to_hardware.hardware_on_hardware.iterator():
                for key in my_hardware_nodes:
                    if from_hardware in my_hardware_nodes[key]:
                        my_dependency = hardware_depending_on_hardware.objects.get(hardware_from=from_hardware,
                                                                                   hardware_to=to_hardware)
                        edge = pydotplus.Edge(from_hardware.name, to_hardware.name)
                        edge.set(
                            'label', my_dependency.port_numbers.replace(',', ';')
                        )
                        graph.add_edge(edge)
        if hardware_type != Hardware.LB:
            graph.add_subgraph(subgraph)

    for to_instance in my_instance_nodes:
        node = pydotplus.Node()
        node.set_name(to_instance.__unicode__())
        node.set('URL', '/instance/%s/' % to_instance.slug)
        node.set('shape', 'component')
        graph.add_node(node)
        for key in my_hardware_nodes:
            for from_hardware in my_hardware_nodes[key]:
                if to_instance in from_hardware.depending_on_instance.iterator():
                    my_dependency = hardware_depending_on_instance.objects.get(from_hardware=from_hardware,
                                                                               to_instance=to_instance)
                    pprint(my_dependency.port_numbers)
                    edge = pydotplus.Edge(from_hardware.name, to_instance.__unicode__())
                    edge.set('headlabel', my_dependency.port_numbers)
                    graph.add_edge(edge)

        if to_instance.customer_accesable:
            edge = pydotplus.Edge('Merchant', to_instance.__unicode__())
            graph.add_edge(edge)

    #
    # Workaround to make SVG responsive
    #
    my_graph = graph.create(format='svg', )
    my_graph = re.sub(r"( width=)", " min-width=", my_graph)
    my_graph = re.sub(r"( height=)", " min-height=", my_graph)

    return my_graph
