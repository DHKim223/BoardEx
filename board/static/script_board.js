$(document).ready(
	function(){
		
		
		
	}
);


	
// 글쓰기
function writecheck(){
	writer = $("input[name=writer]").val();
	subject = $("input[name=subject]").val();
	content = $("textarea").val();
	passwd = $("input[name=passwd]").val();
	if( ! writer) {
		alert("작성자를 입력하세요");
		$("input[name=writer]").focus();
		return false;		
	} else if( ! subject) {
		alert("제목을 입력하세요");
		$("input[name=subject]").focus();
		return false;		
	} else if( ! content ) {
		alert("내용을 입력하세요");
		$("textarea").focus();
		return false;		
	} else if( ! passwd) {
		alert("비밀번호를 입력하세요");
		$("input[name=passwd]").focus();
		return false;		
	}
}