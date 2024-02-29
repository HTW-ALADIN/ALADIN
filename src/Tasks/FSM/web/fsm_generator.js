function generateRandomRegex(difficulty) {
    var regex = "";

    if (difficulty < 3)
        regex = noam.re.string.random(3, "abc", {});
    else if (difficulty < 5)
        regex = noam.re.string.random(4, "abcd", {});
    else if (difficulty < 8)
        regex = noam.re.string.random(difficulty, "abcde", {});
    else
        regex = noam.re.string.random(8, "abcdef", {});

    var regexSimplified = noam.re.string.simplify(regex);

    return regexSimplified;
}


function generateFsmFromRegex(regex) {
    var automaton = noam.re.string.toAutomaton(regex);

    automaton = noam.fsm.convertEnfaToNfa(automaton);
    automaton = noam.fsm.convertNfaToDfa(automaton);
    automaton = noam.fsm.minimize(automaton);
    automaton = noam.fsm.convertStatesToNumbers(automaton);

    var dotString = noam.fsm.printDotFormat(automaton);

    return dotString;
}
