class QuickchartGraphviz {
  static const String _url = 'www.quickchart.io';

  static String getGraphvizImageUrl(String graphInDotNotation) {
    var graphStr = graphInDotNotation.replaceAll('\n', '');

    final queryParameters = {
      'graph': graphStr,
    };

    final uri = Uri.https(_url, '/graphviz', queryParameters);

    return uri.toString();
  }
}