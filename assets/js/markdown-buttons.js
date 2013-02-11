function insertText(before, after)
{
    var textarea = document.getElementById("id_text");
    var sel = rangyInputs.getSelection(textarea);

    rangyInputs.insertText(textarea, before, sel.end);
    rangyInputs.insertText(textarea, after, sel.start);

    rangyInputs.setSelection(textarea, sel.start, sel.end + before.length + after.length);

    textarea.focus();
}

function bold()
{
    insertText("**", "**");
}

function italic()
{
    insertText("*", "*");
}

function code()
{
    insertText("\n```", "```\n");
}
