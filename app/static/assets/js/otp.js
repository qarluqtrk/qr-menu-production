function getCodeBoxElement(index) {
  return document.getElementById("five" + index);
}

function collectOTP() {
  let otp = "";
  for (let index = 1; index <= 6; index++) {
    otp += getCodeBoxElement(index).value;
  }
  return otp;
}

function onKeyUpEvent(index, event) {
  const eventCode = event.which || event.keyCode;
  if (getCodeBoxElement(index).value.length === 1) {
    if (index !== 6) {
      getCodeBoxElement(index + 1).focus();
    } else {
      getCodeBoxElement(index).blur();

      console.log("submit code ");
      const otpCode = collectOTP()
      document.getElementById('otpInput').value = otpCode
      document.getElementById('otpForm').submit()
    }
  }
  if (eventCode === 6 && index !== 1) {
    getCodeBoxElement(index - 1).focus();
  }
}

function onFocusEvent(index) {
  for (item = 1; item < index; item++) {
    const currentElement = getCodeBoxElement(item);
    if (!currentElement.value) {
      currentElement.focus();
      break;
    }
  }
}