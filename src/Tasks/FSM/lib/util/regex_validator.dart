import 'package:fsm_puzzle/util/graphviz_helper.dart';
import 'package:graphviz2/graphviz2.dart';

class RegexValidator {
  final Graph automaton;
  late final GraphvizHelper _gvizHelper;

  RegexValidator({required this.automaton, GraphvizHelper? gvizHelper})
      : _gvizHelper = gvizHelper ?? GraphvizHelper(graph: automaton);

  bool validate(String word) {
    NodeId currentNode = _gvizHelper.nodes[0];
    for (int i = 0; i < word.length; i++) {
      final char = word[i];

      final edgesFromCurrentNode = _gvizHelper.getEdgesFrom(currentNode);

      bool found = false;
      for (var edge in edgesFromCurrentNode) {
        final inputs = _gvizHelper.getInputsOfEdge(edge);
        if (inputs.contains(char)) {
          currentNode = NodeId(edge.rhs.target.toString());
          found = true;
          break;
        }
      }

      if (!found) {
        return false;
      }
    }

    return _gvizHelper.isEndNode(currentNode);
  }
}
