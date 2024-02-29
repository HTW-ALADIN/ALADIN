import 'package:bloc/bloc.dart';
import 'package:flutter/material.dart';
import 'package:fsm_puzzle/pages/question_generator/util/question.dart';
import 'package:fsm_puzzle/pages/question_generator/util/question_set_generator.dart';

part 'question_generator_state.dart';

class QuestionGeneratorCubit extends Cubit<QuestionGeneratorState> {
  QuestionGeneratorCubit()
      : super(
          const QuestionGeneratorState(
            numberOfQuestions: 5,
            difficulty: RangeValues(2, 5),
            questions: null,
          ),
        );

  void onNumberOfQuestionsChanged(int value) {
    emit(state.copyWith(numberOfQuestions: value));
  }

  void onDifficultyChanged(RangeValues value) {
    emit(state.copyWith(difficulty: value));
  }

  List<Question> generateQuestions() {
    final generatedQuestions = QuestionSetGenerator(
      numberOfQuestions: state.numberOfQuestions,
      difficulty: state.difficulty,
    ).generateQuestions();

    emit(state.copyWith(questions: generatedQuestions));
    return generatedQuestions;
  }
}
