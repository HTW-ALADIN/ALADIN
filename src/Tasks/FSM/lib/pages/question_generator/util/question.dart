import 'package:fsm_puzzle/util/graphviz_helper.dart';
import 'package:graphviz2/graphviz2.dart';

class Question {
  Question({
    required this.question,
    required this.graphInDotNotation,
    required this.regex,
  }) {
    final parser = DotParser();
    graph = parser.parseGraph(graphInDotNotation);
    gvizHelper = GraphvizHelper(graph: graph);
    validationStates = List.filled(gvizHelper.edges.length + 2, 0);
  }

  final String question;
  final String graphInDotNotation;
  final String regex;
  late final Graph graph;
  late final GraphvizHelper gvizHelper;
  late List<int> validationStates;

  int get achievedScore => validationStates.reduce((a, b) => a + b);
  int get totalScore => validationStates.length + 2; // add 2 => word and regex get 2 points each
}