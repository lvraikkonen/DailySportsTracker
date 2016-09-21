// try to use javascript for data visulization
var paragraphs = document.getElementsByTagName("p");
for (var i = 0; i < paragraphs.length; i++)
{
    var paragraph = paragraphs.item(i);
    paragraph.innerHTML = "I like js!";
}

// 使用 d3.select() 或 d3.selectAll() 选择元素后返回的对象，就是选择集
var p = d3.select("body")
          .selectAll("p")
          .text("Hello d3.js!");
p.style("color", "red")
 .style("font-size", "72px");

// 绑定数据
var dataset = ["i like bird", "i like cat", "i like dog"];
var p = d3.select("body").selectAll("p");
// 绑定一个数组到选择集上，数组的各项值分别与选择集的各元素绑定
 p.data(dataset)
  .text(function(d, i){
                 return d;
             })
 .style("color", "red");

 // select选取一个元素   selectAll选取全部元素

// select 和 selectAll 的参数符合 CSS 选择器的条件
// 即用“井号（#）”表示 id，用“点（.）”表示 class
var p1 = d3.select("body").selectAll(".myclass");
p1.style("color", "red");

var p2 = d3.select("p#pe");
p2.style("color", "red");

// 追加元素
d3.select("body").append("p").text("new paragraph");
// 在指定位置添加元素
d3.select("body").insert("p", "#pe").text("new before Pear");
// 删除元素
p_deleted = d3.select("body").select(".myclass");
p_deleted.remove();

// 添加画布SVG
var width = 300;
var height = 300;

var svg = d3.select("body")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
