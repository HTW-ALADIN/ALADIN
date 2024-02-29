import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:fsm_puzzle/pages/home/home_page.dart';
import 'package:fsm_puzzle/pages/question_generator/cubit/question_generator_cubit.dart';
import 'package:fsm_puzzle/pages/question_viewer/question_viewer_page.dart';
import 'package:fsm_puzzle/pages/summary/summary_page.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider(create: (context) => QuestionGeneratorCubit()),
      ],
      child: MaterialApp(
        title: 'FSM Puzzle',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
          useMaterial3: true,
        ),
        routes: {
          '/': (context) => const HomePage(),
          '/question': (context) => QuestionViewerPage(
                questions:
                    context.read<QuestionGeneratorCubit>().generateQuestions(),
              ),
          '/summary': (context) => SummaryPage(
              questions:
                  context.read<QuestionGeneratorCubit>().state.questions ?? []),
        },
      ),
    );
  }
}
