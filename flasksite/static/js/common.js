var ds = {};
ds.convertDate = function(date) {
var converted = new Date(date);
converted.setTime(converted.getTime() + converted.getTimezoneOffset() * 60 * 1000);
return converted;
};
