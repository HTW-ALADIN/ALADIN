import 'dart:math';

import 'package:flutter/material.dart';
import 'package:fsm_puzzle/pages/question_generator/util/question.dart';
import 'package:fsm_puzzle/pages/question_generator/util/question_generator.dart';

class QuestionSetGenerator {
  QuestionSetGenerator({
    required this.numberOfQuestions,
    required this.difficulty,
  });

  final int numberOfQuestions;
  final RangeValues difficulty;

  List<Question> generateQuestions() {
    final questions = List<Question>.empty(growable: true);

    for (var i = 0; i < numberOfQuestions; i++) {
      final randomDifficulty = Random(DateTime.now().millisecondsSinceEpoch)
              .nextInt(difficulty.end.toInt() - difficulty.start.toInt() + 1) +
          difficulty.start.toInt();

      questions.add(
        QuestionGenerator(difficulty: randomDifficulty).generateQuestion(),
      );
    }

    return questions;
  }
}
