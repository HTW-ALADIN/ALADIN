import 'dart:math';

import 'package:flutter/material.dart';
import 'package:fsm_puzzle/pages/question_generator/util/question.dart';
import 'package:gap/gap.dart';

class SummaryPage extends StatefulWidget {
  const SummaryPage({
    super.key,
    required this.questions,
  });

  final List<Question> questions;

  @override
  _SummaryPageState createState() => _SummaryPageState();
}

class _SummaryPageState extends State<SummaryPage> {
  Widget buildResult(int questionNumber, int achievedScore, int totalScore) {
    return Padding(
      padding: const EdgeInsets.all(5.0),
      child: SizedBox(
        width: 200,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text('$questionNumber. Task: $achievedScore / $totalScore',
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                    )),
            const Gap(10),
            Transform.rotate(
              angle: achievedScore == totalScore ? 0 : pi / 4,
              child: Icon(
                achievedScore == totalScore
                    ? Icons.check_circle_outline
                    : Icons.add_circle_outline,
                color: achievedScore == totalScore ? Colors.green : Colors.red,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget buildTotalScore(int achievedScore, int totalScore) {
    return Padding(
      padding: const EdgeInsets.all(5.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            'Total Score: $achievedScore / $totalScore',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
          ),
          const Gap(10),
        ],
      ),
    );
  }

  List<Widget> _buildResults(List<Question> questions) {
    final results = <Widget>[];
    for (var i = 0; i < questions.length; i++) {
      results.add(buildResult(
        i + 1,
        questions[i].achievedScore,
        questions[i].totalScore,
      ));
    }
    return results;
  }

  @override
  Widget build(BuildContext context) {
    print(widget.questions.map((e) => e.validationStates));
    return Scaffold(
        appBar: AppBar(),
        body: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Gap(50),
            Text(
              'Summary',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const Gap(20),
            ..._buildResults(widget.questions),
            const Gap(10),
            buildTotalScore(
                widget.questions
                    .map((e) => e.achievedScore)
                    .reduce((v, q) => v + q),
                widget.questions
                    .map((e) => e.totalScore)
                    .reduce((v, q) => v + q)),
            const Gap(50),
            TextButton(
              onPressed: () => Navigator.of(context).pushNamed('/'),
              child: const Text('Back to Generator',
                  style: TextStyle(fontSize: 20)),
            ),
          ],
        ));
  }
}
