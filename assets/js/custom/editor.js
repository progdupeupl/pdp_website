/* Adds an useful `startsWith` function to the `String` prototype if it does
 * not exists yet.
 */
if (typeof String.prototype.startsWith != 'function') {
	String.prototype.startsWith = function (str) {
		return this.indexOf(str) == 0;
	};
}



var indentString = "    ";



/* Returns an object which contains the selection bounds.
 *
 * lines: An array of the lines.
 *
 * selectionStart: The index of the first character in the selection from the
 * beginning of the first line
 *
 * selectionEnd: The index of the last character in the selection
 */
function getLineSelection(lines, selectionStart, selectionEnd) {

	var selection = {
		start: -1,
		end: -1,
	};

	// The index of the first character of the current line
	var lineStartIndex = 0;
	// The index of the last character of the current line
	var lineEndIndex;

	for (var i = 0; i < lines.length; i++) {

		var line = lines[i];
		lineEndIndex = lineStartIndex + line.length;

		if (lineStartIndex <= selectionEnd
				&& lineEndIndex >= selectionStart) {

			// We are in the selection, set up `selection.start` if -1
			if (selection.start == -1) {
				selection.start = i;
			}

		} else {

			if (selection.start != -1) {
				// We have exited the selection
				selection.end = i - 1;
				return selection;
			}

		}

		lineStartIndex = lineEndIndex + 1; // 1 is the line feed character size
	}

	if (selection.start == -1)
		throw "Error";

	selection.end = lines.length - 1;
	return selection;
}



function isLineSelected(lineIndex, lineSelection) {
	return lineSelection.start <= lineIndex && lineSelection.end >= lineIndex;
}



function createSimpleIndenter(indentString) {
	var indenter = function() {
		return indentString;
	};
	return indenter;
}



/*
 * lines: An array of the lines
 *
 * lineSelection: An object which contains the selection bounds, returned by
 * `getLineSelection`
 *
 * indenter: A function which returns the string added to shift right.
 *
 * Returns an object which contains :
 *
 *		lines: An array of the modified lines
 *
 *		addedCharCount: The number of added characters (negative if characters
 *			have been removed)
 *
 *		addedCharCountFirstLine: The number of added characters to the first
 *			line of the selection (can be negative too).
 */
function shiftRightLineSelection(lines, lineSelection, indenter) {

	var newLines = [];
	var addedCharCount = 0;
	var firstLineIndent = null;

	for (var i = 0; i < lines.length; i++) {
		var newLine = lines[i];
		if (isLineSelected(i, lineSelection)) {
			var indentString = indenter();
			if (firstLineIndent === null) {
				firstLineIndent = indentString;
			}
			newLine = indentString + newLine;
			addedCharCount += indentString.length;
		}
		newLines.push(newLine);
	}

	return {
		lines: newLines,
		addedCharCount: addedCharCount,
		addedCharCountFirstLine: firstLineIndent.length,
	};
}



/*
 * lines: An array of the lines
 *
 * lineSelection: An object which contains the selection bounds, returned by
 * `getLineSelection`
 *
 *
 * Returns an object which contains :
 *
 *		lines: An array of the modified lines
 *
 *		addedCharCount: The number of added characters (negative if characters
 *			have been removed)
 *
 *		addedCharCountFirstLine: The number of added characters to the first
 *			line of the selection (can be negative too).
 */
function shiftLeftLineSelection(lines, lineSelection) {

	var newLines = [];
	var addedCharCount = 0;
	var addedCharCountFirstLine = null

	for (var i = 0; i < lines.length; i++) {
		var newLine = lines[i];
		if (isLineSelected(i, lineSelection)) {

			var indentSize = 0;

			if (newLine.startsWith(indentString)) {
				indentSize = indentString.length
			} else if (newLine.startsWith(" ") || newLine.startsWith("\t")) {
				indentSize = 1
			}

			if (addedCharCountFirstLine === null) {
				addedCharCountFirstLine = -indentSize;
			}
			newLine = newLine.substring(indentSize, newLine.length);
			addedCharCount -= indentSize;
		}
		newLines.push(newLine);
	}

	return {
		lines: newLines,
		addedCharCount: addedCharCount,
		addedCharCountFirstLine: addedCharCountFirstLine,
	};
}



function textAreaTabPressed(textArea, event) {

	var scroll = this.scrollTop;

	if(textArea.selectionStart == textArea.selectionEnd) {
		// Nothing is selected, nothing to indent. Just set the focus to
		// the submit button
		return true;
	}

	var oldSelectionStart = textArea.selectionStart;
	var oldSelectionEnd = textArea.selectionEnd;

	var	lines = textArea.value.split("\n");
	var lineSelection = getLineSelection(lines,
	        textArea.selectionStart, textArea.selectionEnd);

	var indenter = createSimpleIndenter(indentString);

	var res = event.shiftKey ?
			shiftLeftLineSelection(lines, lineSelection)
			: shiftRightLineSelection(lines, lineSelection, indenter);

	var newLines = res.lines;
	var addedCharCount = res.addedCharCount;
	var addedCharCountFirstLine = res.addedCharCountFirstLine

	var newText = newLines.join("\n");

	textArea.value = newText;

	textArea.setSelectionRange(
			oldSelectionStart + addedCharCountFirstLine,
			oldSelectionEnd + addedCharCount);

	//textArea.focus();
	//textArea.scrollTop = scroll;

	// Cancel the action of the tabulator key, avoid to set the focus to
	// the next focusable element.
	return false;

}



/* Adds observers on each text area */
function addTabObservers() {

	var textareas = document.getElementsByTagName("textarea");

	for(var i = 0, t = textareas.length; i < t; i++){

		textareas[i].onkeydown = function(event) {
			var isTabDown = (event || window.event).keyCode == 9;
			if (isTabDown) {
				return textAreaTabPressed(this, event || window.event);
			}
		};
	}
}

addTabObservers();



//var textar="id_description";

function bold(textAreaId) {
	surroundSelection(textAreaId, "**", "**");
}

function italic(textAreaId) {
	surroundSelection(textAreaId, "*", "*");
}

function ed_title(textAreaId, level) {
    var start = "";
    for(var i = 0; i < level; i++) {
        start = start + "#";
    }
    surroundSelection(textAreaId, start + " ", "");
}

function link(textAreaId) {
	var url = prompt('Saisissez l’adresse du lien :', 'http://');
	if (! url)
		return;
	surroundSelection(textAreaId, "[", "](" + url + ")");
}

function secret(textAreaId) {
	surroundSelection(textAreaId, "\n[secret]{\n", "\n}\n");
}

function image(textAreaId) {
	var url = prompt('Saisissez l’URL de l’image :', 'http://');
	if (! url)
		return;
	surroundSelection(textAreaId, "![", "](" + url + ")");
}


function bulletList(textAreaId) {
	shiftRightAndSurroundSelection(textAreaId, createSimpleIndenter(" - "),
			'\n', '\n');
}

function numericList(textAreaId) {
	var index = 1;
	var indenter = function() {
		return ' ' + (index++) + '. ';
	}
	shiftRightAndSurroundSelection(textAreaId, indenter, '\n', '\n');
}


function quote(textAreaId) {

	var author = prompt('Saisissez l’auteur de la citation :\n'
			+ 'Laissez vide pour créer une citation anonyme.', '');

	var indenter = createSimpleIndenter("> ");

	if (author) {
		author = author.trim();
		if (author.length != 0) {
			shiftRightAndSurroundSelection(textAreaId, indenter,
					'\n**' + author + ' a écrit :**\n', '\n');
			return;
		}
	}

	shiftRightAndSurroundSelection(textAreaId, indenter, '\n', '\n');
}


function code(textAreaId) {

	var code = prompt('Entrez le nom du langage '
	      + '(c, c++, java, python, php, html, ...) :', '');

	if (! code)
		code = '';
	surroundSelection(textAreaId,
			'\n```' + code.trim().toLowerCase() + '\n',
			'\n```\n');
}


function inlineCode(textAreaId) {
	surroundSelection(textAreaId, '`', '`');
}



/* Surrounds the selection between `prefix` and `suffix`.
 * textAreaId: The id of the text area HTML element.
 */
function surroundSelection(textAreaId, prefix, suffix) {

	var textArea = document.getElementById(textAreaId);
	var scroll = textArea.scrollTop;

	var beforeSelection = textArea.value.substring(0, textArea.selectionStart);
	var selection = textArea.value.substring(
	        textArea.selectionStart, textArea.selectionEnd);
	var afterSelection = textArea.value.substring(textArea.selectionEnd);

	textArea.value = beforeSelection + prefix + selection + suffix + afterSelection;

	textArea.setSelectionRange(
			beforeSelection.length + prefix.length,
			beforeSelection.length + prefix.length + selection.length);

	// textArea.focus();
	// textArea.scrollTop = scroll;
}



/* Surrounds the selection between `prefix` and `suffix`.
 * textAreaId: The id of the text area HTML element.
 * indenter: A function which returns the string added to shift right.
 */
function shiftRightAndSurroundSelection(textAreaId, indenter, prefix, suffix) {

	surroundSelection(textAreaId, prefix, suffix);

	var textArea = document.getElementById(textAreaId);
	var scrollTop = textArea.scrollTop;

	var oldSelectionStart = textArea.selectionStart;
	var oldSelectionEnd = textArea.selectionEnd;

	var	lines = textArea.value.split("\n");
	var lineSelection = getLineSelection(lines,
			textArea.selectionStart, textArea.selectionEnd);

	var res = shiftRightLineSelection(lines, lineSelection, indenter);

	var newLines = res.lines;
	var addedCharCount = res.addedCharCount;
	var addedCharCountFirstLine = res.addedCharCountFirstLine

	var newText = newLines.join("\n");
	textArea.value = newText;

	textArea.setSelectionRange(
			oldSelectionStart + addedCharCountFirstLine,
			oldSelectionEnd + addedCharCount);

	//textArea.focus();
	//textArea.scrollTop = scroll;

	return true;
}

