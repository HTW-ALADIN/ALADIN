import 'package:flutter/material.dart';
import 'package:fsm_puzzle/pages/question_generator/util/question.dart';
import 'package:fsm_puzzle/pages/question_viewer/question_view.dart';
import 'package:gap/gap.dart';

class QuestionViewerPage extends StatefulWidget {
  const QuestionViewerPage({
    required this.questions,
    super.key,
  });

  final List<Question> questions;

  @override
  _QuestionViewerPageState createState() => _QuestionViewerPageState();
}

class _QuestionViewerPageState extends State<QuestionViewerPage> {
  int _currentQuestionIndex = 0;
  late ValueNotifier<List<int>> _validationNotifier;

  Question get _currentQuestion => widget.questions[_currentQuestionIndex];

  @override
  void initState() {
    super.initState();
    _validationNotifier = ValueNotifier(_currentQuestion.validationStates);
  }

  void onForwardNavigation() {
    widget.questions[_currentQuestionIndex].validationStates =
        _validationNotifier.value;
    setState(() {
      if (_currentQuestionIndex < widget.questions.length - 1) {
        _currentQuestionIndex++;
        _validationNotifier.value = _currentQuestion.validationStates;
      } else {
        Navigator.pushNamed(context, '/summary');
      }
    });
  }

  void onBackwardNavigation() {
    if (_currentQuestionIndex > 0) {
      setState(() {
        _currentQuestionIndex--;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      floatingActionButton: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          OutlinedButton(
            onPressed: onBackwardNavigation,
            child: const Icon(Icons.navigate_before),
          ),
          Text('${_currentQuestionIndex + 1} / ${widget.questions.length}'),
          OutlinedButton(
            onPressed: onForwardNavigation,
            child: const Icon(Icons.navigate_next),
          ),
        ],
      ),
      body: Center(
        child: Column(
          children: [
            const Gap(30),
            Builder(
              builder: (context) {
                return QuestionView(
                  key: ValueKey(_currentQuestionIndex),
                  question: _currentQuestion,
                  validationNotifier: _validationNotifier,
                );
              }
            ),
          ],
        ),
      ),
    );
  }
}
