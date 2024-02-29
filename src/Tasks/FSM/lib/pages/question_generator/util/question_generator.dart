import 'package:fsm_puzzle/pages/question_generator/util/fsm_generator.dart';
import 'package:fsm_puzzle/pages/question_generator/util/question.dart';

class QuestionGenerator {
  QuestionGenerator({
    required this.difficulty,
  });

  final int difficulty;

  Question generateQuestion() {
    final fsmGenerator = FsmGenerator();
    fsmGenerator.generateFsmNoam(difficulty: difficulty);
    return Question(
      question: 'Fill the state table for the following FSM:',
      graphInDotNotation:
          fsmGenerator.dotNotation ?? (throw Exception('dotNotation is null')),
      regex: fsmGenerator.regex ?? (throw Exception('regex is null')),
    );
  }
}
