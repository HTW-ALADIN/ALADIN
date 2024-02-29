import 'package:flutter/services.dart';
import 'package:graph_dot/graph_dot.dart';
import 'package:http/http.dart' as http;
import 'dart:js' as js;

class FsmGenerator {
  String? regex;
  String? dotNotation;

  void generateFsmNoam({required int difficulty}) {
    regex =
        js.context.callMethod('generateRandomRegex', [difficulty]).toString();

    print('Dart regex: $regex');

    dotNotation = js.context.callMethod('generateFsmFromRegex', [regex]);

    print('Dart dotNotation: $dotNotation');
  }

  Future<Graph> generateFsmDummy({required int numberOfStates}) async {
    //JavascriptRuntime runtime = getJavascriptRuntime();

    /*
    final scriptUrl = 'https://ivanzuzak.info/noam/lib/browser/noam.js';
    // fetch script from the web
    final script = await http.get(Uri.parse(scriptUrl));

    final regex = 'aba';

    final result = runtime.evaluate('''${script.body}noam.re.string.toAutomaton($regex);''');
*/
    regex = '((ab)+c)d';
/*
    final file = await rootBundle.loadString("assets/lexical.js");



    final result = runtime.evaluate('''${file}regexToNfa("$regex")''');

    print(result.rawResult);

*/

    // for input: ((ab)+c)d
    final graph = Graph();
    graph.setNode('s0', label: 's0');
    graph.setNode('s1', label: 's1');
    graph.setNode('s2', label: 's2');
    graph.setNode('s3', label: 's3');
    graph.setNode('s4', label: 's4');

    graph.setEdge('s0', 's1', label: 'c');
    graph.setEdge('s0', 's3', label: 'a');
    graph.setEdge('s0', 's4', label: 'b,d');
    graph.setEdge('s1', 's2', label: 'd');
    graph.setEdge('s3', 's1', label: 'b');

    graph.setEdge('s0', 's4', label: 'b,d');
    graph.setEdge('s1', 's4', label: 'a,b,c');
    graph.setEdge('s2', 's4', label: 'a,b,c,d');
    graph.setEdge('s3', 's4', label: 'a,c,d');
    graph.setEdge('s4', 's4', label: 'a,b,c,d');

    dotNotation = graph.toDot();

    return graph;
  }
}
