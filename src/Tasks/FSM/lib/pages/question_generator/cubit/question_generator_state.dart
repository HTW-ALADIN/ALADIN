part of 'question_generator_cubit.dart';

@immutable
class QuestionGeneratorState {
  final int numberOfQuestions;
  final RangeValues difficulty;
  final List<Question>? questions;

  const QuestionGeneratorState({
    required this.numberOfQuestions,
    required this.difficulty,
    required this.questions,
  });

  copyWith({
    int? numberOfQuestions,
    RangeValues? difficulty,
    List<Question>? questions,
  }) {
    return QuestionGeneratorState(
      numberOfQuestions: numberOfQuestions ?? this.numberOfQuestions,
      difficulty: difficulty ?? this.difficulty,
      questions: questions,
    );
  }
}
