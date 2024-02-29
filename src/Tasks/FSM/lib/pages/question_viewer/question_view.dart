import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:fsm_puzzle/pages/question_generator/util/question.dart';
import 'package:fsm_puzzle/util/graphviz_helper.dart';
import 'package:fsm_puzzle/util/quickchart_graphviz.dart';
import 'package:fsm_puzzle/util/regex_validator.dart';
import 'package:gap/gap.dart';
import 'package:graphviz2/graphviz2.dart';

class QuestionView extends StatefulWidget {
  const QuestionView(
      {required this.question, required this.validationNotifier, super.key});

  final Question question;
  final ValueNotifier<List<int>> validationNotifier;

  @override
  State<QuestionView> createState() => _QuestionViewState();
}

class _QuestionViewState extends State<QuestionView> {
  final _formKey = GlobalKey<FormState>();
  late final List<int> _validationStates;
  late final GraphvizHelper _gvizHelper;

  @override
  void initState() {
    super.initState();

    _gvizHelper = widget.question.gvizHelper;
    _validationStates = List.filled(_gvizHelper.edges.length + 2, 0);
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text(
          widget.question.question,
          style: Theme.of(context).textTheme.headlineSmall,
        ),
        // TODO: remove for production
        Text(
          'Regex hint: ${widget.question.regex}',
          style: Theme.of(context)
              .textTheme
              .bodySmall
              ?.copyWith(color: Colors.grey),
        ),
        SvgPicture.network(
          QuickchartGraphviz.getGraphvizImageUrl(
            widget.question.graphInDotNotation,
          ),
          width: size.width * 0.8,
          height: size.height * 0.35,
          fit: BoxFit.scaleDown,
        ),
        SizedBox(
          height: size.height * 0.65 - 200,
          child: Form(
            key: _formKey,
            autovalidateMode: AutovalidateMode.always,
            onChanged: () {
              _formKey.currentState?.validate();
              widget.validationNotifier.value = _validationStates;
            },
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.end,
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                SizedBox(
                  width: size.width * 0.6,
                  child: GridView.count(
                    crossAxisCount: 3,
                    shrinkWrap: true,
                    mainAxisSpacing: 0,
                    childAspectRatio: 8,
                    children: [
                      _buildTableItemText('State'),
                      _buildTableItemText('Input'),
                      _buildTableItemText('Next State'),
                      ..._buildTableContent(),
                    ],
                  ),
                ),
                SizedBox(
                  width: size.width * 0.2,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      const Text(
                          'Enter a word which gets accepted by the FSM:'),
                      const Gap(5),
                      TextFormField(
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                        ),
                        validator: _wordValidator,
                      ),
                      const Gap(30),
                      const Text('Enter the Regex that describes the FSM:'),
                      const Gap(5),
                      TextFormField(
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                        ),
                        validator: _regexValidator,
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildTableItemText(String text) {
    return Container(
      alignment: Alignment.center,
      decoration: BoxDecoration(
        border: Border.all(color: Colors.black),
      ),
      child: Text(text),
    );
  }

  List<Widget> _buildTableContent() {
    final List<Widget> tableContent = [];
    int textFieldsCount = 0;

    for (var i = 0; i < _gvizHelper.nodes.length; i++) {
      for (var j = 0;
          j < _gvizHelper.getInputsAt(_gvizHelper.nodes[i]).length;
          j++) {
        tableContent.add(_buildTableItemText(_gvizHelper.nodes[i].toString()));
        tableContent.add(_buildTableItemText(
            _gvizHelper.getInputsAt(_gvizHelper.nodes[i])[j]));
        tableContent.add(ValidatabelTextField(
          id: textFieldsCount,
          origin: _gvizHelper.nodes[i],
          label: _gvizHelper.getInputsAt(_gvizHelper.nodes[i])[j],
          edgeExists: _gvizHelper.edgeExists,
          setValidation: (id, value) {
            _validationStates[id] = value;
          },
        ));
        textFieldsCount++;
      }
    }
    return tableContent;
  }

  String? _wordValidator(String? value) {
    if (value == null || value.isEmpty) {
      _validationStates[_validationStates.length - 2] = 0;
      return null;
    }
    if (!RegexValidator(
      automaton: widget.question.graph,
      gvizHelper: _gvizHelper,
    ).validate(value)) {
      _validationStates[_validationStates.length - 2] = 0;
      return 'Invalid input';
    }
    _validationStates[_validationStates.length - 2] = 2;
    return null;
  }

  String? _regexValidator(String? value) {
    if (value == null || value.isEmpty) {
      _validationStates[_validationStates.length - 1] = 0;
      return null;
    }
    if (value != widget.question.regex) {
      _validationStates[_validationStates.length - 1] = 0;
      return 'Invalid regex';
    }
    _validationStates[_validationStates.length - 1] = 2;
    return null;
  }
}

class ValidatabelTextField extends StatelessWidget {
  const ValidatabelTextField(
      {required this.id,
      required this.origin,
      required this.label,
      required this.edgeExists,
      required this.setValidation,
      super.key});

  final int id;
  final NodeId origin;
  final String label;
  final bool Function({
    required NodeId origin,
    required String label,
    required NodeId destination,
  }) edgeExists;
  final void Function(int id, int value) setValidation;

  String? validator(String? value) {
    if (value == null || value.isEmpty) {
      setValidation(id, 0);
      return null;
    }
    if (!edgeExists(
      origin: origin,
      label: label,
      destination: NodeId(value),
    )) {
      setValidation(id, 0);
      return 'Invalid state';
    }

    setValidation(id, 1);

    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.center,
      decoration: BoxDecoration(
        border: Border.all(color: Colors.black),
      ),
      child: TextFormField(
        decoration: const InputDecoration(
          border: OutlineInputBorder(),
        ),
        validator: validator,
      ),
    );
  }
}
