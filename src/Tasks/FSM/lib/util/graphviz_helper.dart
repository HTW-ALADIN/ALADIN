import 'package:graphviz2/graphviz2.dart';

class GraphvizHelper {
  GraphvizHelper({required this.graph});

  final Graph graph;

  List<EdgeStatement>? _edges;

  List<EdgeStatement> get edges => _edges ?? (_edges = _getEdges());

  List<NodeId>? _nodes;

  List<NodeId> get nodes => _nodes ?? (_nodes = _getNodes());

  List<NodeId>? _endNodes;

  List<NodeId> get endNodes => _endNodes ?? (_endNodes = _getEndNodes());

  List<EdgeStatement> _getEdges() => graph.stmtList.statements
      .whereType<EdgeStatement>()
      .where((e) => e.origin != const NodeId('secret_node'))
      .toList();

  List<NodeId> _getNodes() {
    final nodes = <NodeId>[];

    for (final e in edges) {
      if (nodes.contains(e.origin) == false) {
        nodes.add(NodeId(e.origin.toString()));
      }
    }
    nodes.sort((a, b) => a.id.toLowerCase().compareTo(b.id.toLowerCase()));
    return nodes;
  }

  List<String> getInputsAt(NodeId node) {
    final inputs = <String>[];

    final edgesAtNode = getEdgesFrom(node);

    for (final e in edgesAtNode) {
      final edgeLabel = _getLabelFromAttrList(e.attrList);
      if (edgeLabel != null && inputs.contains(edgeLabel) == false) {
        inputs.add(edgeLabel);
      }
    }

    return inputs;
  }

  List<EdgeStatement> getEdgesFrom(NodeId node) {
    final edges = <EdgeStatement>[];
    for (final e in this
        .edges
        .where((e) => !(e.attrList?.aLists.any((e) =>
                e.properties.containsKey('dir') &&
                e.properties['dir'] == 'back') ??
            true))
        .where((e) => e.origin == node)) {
      edges.add(e);
    }

    for (final e in this
        .edges
        .where((e) =>
            e.attrList?.aLists.any((e) =>
                e.properties.containsKey('dir') &&
                e.properties['dir'] == 'back') ??
            false)
        .where((e) => e.rhs.target == node)) {
      edges.add(e);
    }

    return edges;
  }

  List<String> getInputsOfEdge(EdgeStatement edge) {
    final edgeLabel = _getLabelFromAttrList(edge.attrList);
    return edgeLabel?.split(',') ?? [];
  }

  bool edgeExists({
    required NodeId origin,
    required String label,
    required NodeId destination,
  }) {
    final edgesAtOrigin = getEdgesFrom(origin);
    final hasEdgeInNormaDir = edgesAtOrigin.any((e) =>
        _getLabelFromAttrList(e.attrList) == label &&
        e.rhs.target == destination &&
        !(e.attrList?.aLists.any((e) =>
                e.properties.containsKey('dir') &&
                e.properties['dir'] == 'back') ==
            true));

    final hasEdgeInBackDir = edgesAtOrigin.any((e) =>
        _getLabelFromAttrList(e.attrList) == label &&
        e.origin == destination &&
        e.attrList?.aLists.any((e) =>
                e.properties.containsKey('dir') &&
                e.properties['dir'] == 'back') ==
            false);

    return hasEdgeInNormaDir || hasEdgeInBackDir;
  }

  String? _getLabelFromAttrList(AttrList? attrList) {
    return attrList?.aLists.firstOrNull?.properties['label']
        ?.replaceAll('"', '');
  }

  bool isEndNode(NodeId node) => endNodes.contains(node);

  List<NodeId> _getEndNodes() {
    List<NodeId> endNodes = [];
    bool inDoubleCircleRange = false;
    for (final statement in graph.stmtList.statements) {
      if (statement is AttrStatement &&
          statement.attrList.aLists
              .map((e) => e.properties['shape'])
              .contains('doublecircle')) {
        inDoubleCircleRange = true;
      } else if (statement is AttrStatement &&
          statement.attrList.aLists
              .map((e) => e.properties['shape'])
              .contains('circle')) {
        inDoubleCircleRange = false;
      }

      if (inDoubleCircleRange && statement is NodeStatement) {
        endNodes.add(statement.id);
      }
    }
    return endNodes;
  }
}
