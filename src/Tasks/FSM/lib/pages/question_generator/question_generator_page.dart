import 'package:flutter/material.dart';
import 'package:fsm_puzzle/pages/question_generator/cubit/question_generator_cubit.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gap/gap.dart';

class QuestionGeneratorPage extends StatelessWidget {
  const QuestionGeneratorPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Generate a Question Set'),
      ),
      body: Center(
        child: SizedBox(
          width: (MediaQuery.of(context).size.width * 0.7).clamp(0, 700),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              _buildNumberOfQuestionsSection(context),
              const Gap(10),
              _buildDifficultySection(context),
              const Gap(20),
              TextButton(
                onPressed: () => Navigator.of(context).pushNamed('/question'),
                child: const Text('Start', style: TextStyle(fontSize: 20)),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildNumberOfQuestionsSection(BuildContext context) {
    return BlocBuilder<QuestionGeneratorCubit, QuestionGeneratorState>(
      buildWhen: (previous, current) =>
          previous.numberOfQuestions != current.numberOfQuestions,
      builder: (context, state) {
        return Column(
          children: [
            Text('Number of Questions: ${state.numberOfQuestions}'),
            Slider(
              value: state.numberOfQuestions.toDouble(),
              divisions: 10,
              min: 1,
              max: 10,
              onChanged: (value) => context
                  .read<QuestionGeneratorCubit>()
                  .onNumberOfQuestionsChanged(value.toInt()),
            ),
          ],
        );
      },
    );
  }

  Widget _buildDifficultySection(BuildContext context) {
    return BlocBuilder<QuestionGeneratorCubit, QuestionGeneratorState>(
      buildWhen: (previous, current) =>
          previous.difficulty != current.difficulty,
      builder: (context, state) {
        return Column(
          children: [
            const Text('Difficulty'),
            RangeSlider(
              values: state.difficulty,
              divisions: 10,
              min: 0,
              max: 10,
              onChanged:
                  context.read<QuestionGeneratorCubit>().onDifficultyChanged,
            ),
          ],
        );
      },
    );
  }
}
