//script takes json data and creates lists in html

//makes header
var theDiv = document.getElementById("content");
function makeHeader(obj) {
  var p_space = document.createElement('p');
  var txtNode = document.createTextNode(obj.header.replace(/_/g, ' '));
  var h2 = document.createElement('h2');
  theDiv.appendChild(p_space)
  h2.appendChild(txtNode)
  theDiv.appendChild(h2)
}

//make list
function makeUL(obj, index) {
  var p_space = document.createElement('p');
  var p = document.createElement('p');
  var p_txt = document.createTextNode(Object.keys(obj.item_list[index]));
  var ul = document.createElement('ul');
  var item_list = obj.item_list[index][Object.keys(obj.item_list[index])];
  theDiv.appendChild(p_space)
  p.appendChild(p_txt)
  theDiv.appendChild(p)
  theDiv.appendChild(ul)

  for (var x in item_list) {
    var inner_il = document.createElement('li');
    ul.appendChild(inner_il)
    inner_il.innerHTML = x.replace('female','Feminine').replace('male', 'Masculine') + ': '+ item_list[x];
  }
}

makeHeader(action_gender);
for (i=0;i<action_gender.item_list.length;i++) {
  makeUL(action_gender,i);
}

makeHeader(cause_gender);
for (i=0;i<cause_gender.item_list.length;i++) {
  makeUL(cause_gender,i);
}

makeHeader(action_income);
for (i=0;i<action_income.item_list.length;i++) {
  makeUL(action_income,i);
}

makeHeader(cause_income);
for (i=0;i<cause_income.item_list.length;i++) {
  makeUL(cause_income,i);
}
