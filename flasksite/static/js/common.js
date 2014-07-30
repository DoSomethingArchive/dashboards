var convertDate = function(date) {
    var converted = new Date(date);
    return converted.setTime(converted.getTime() + converted.getTimezoneOffset() * 60 * 1000);
};
