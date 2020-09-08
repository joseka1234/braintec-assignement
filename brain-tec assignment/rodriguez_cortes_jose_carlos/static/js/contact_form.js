$(document).ready(function () {
    $(window).keydown(function (event) {
        if (event.keyCode == 13) {
            event.preventDefault();
            return false;
        }
    });
});

function setValid(element) {
    $(element).addClass("is-valid");
    $(element).removeClass("is-invalid");
}

function setInvalid(element) {
    $(element).addClass("is-invalid");
    $(element).removeClass("is-valid");
}

function checkSubmitButton() {
    if (isDataCorrect()) {
        $("#input_button").prop("disabled", false);
        $("#message_correct_data").removeClass("invisible")
    } else {
        $("#input_button").prop("disabled", true);
        $("#message_correct_data").addClass("invisible")
    }
}

function isDataCorrect() {
    var email = $("#email").val();
    var phone = $("#phone").val();
    var valid_name = !isEmptyString($("#firstname").val());
    var valid_lastname = !isEmptyString($("#lastname").val());
    var valid_email = !isEmptyString(email) && isCorrectEmail(email);
    var valid_phone = isEmptyString(phone) || isCorrectPhone(phone);
    return valid_name && valid_lastname && valid_email && valid_phone;
}

$("#firstname").change(() => {
    if (!isEmptyString($("#firstname").val())) {
        setValid("#firstname");
    } else {
        setInvalid("#firstname");
    }
    checkSubmitButton();
});

$("#lastname").change(() => {
    if (!isEmptyString($("#lastname").val())) {
        setValid("#lastname");
    } else {
        setInvalid("#lastname");
    }
    checkSubmitButton();
});

$("#email").change(() => {
    var email = $("#email").val();
    if (!isEmptyString(email) && isCorrectEmail(email)) {
        setValid("#email");
    } else {
        setInvalid("#email");
    }
    checkSubmitButton();
});

$("#phone").change(() => {
    var phone = $("#phone").val();
    if (!isEmptyString(phone) && isCorrectPhone(phone)) {
        setValid("#phone");
    } else {
        setInvalid("#phone");
    }
    checkSubmitButton()
});

$("#address").change(() => {
    if (!isEmptyString($("#address").val())) {
        setValid("#address");
    } else {
        setInvalid("#address");
    }
});

function isCorrectPhone(phone) {
    return /^\+*[-\s()0-9]+$/.test(phone);
}

function isCorrectEmail(email) {
    return /^.+@.+\..+$/.test(email);
}

function isEmptyString(str) {
    return !str || str.length === 0;
}

$("#xml_file").change(() => $("#xml_form").submit());