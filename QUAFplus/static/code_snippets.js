document.addEventListener("DOMContentLoaded",()=>{
    var out=(e)=>{
	return(t)=>{
	    e.getElementsByClassName("code_out").item(0).innerHTML+=t.replace("\n","<br>");
	};
    };
    var py_eventify=(e)=>{
	let q=e;
	console.log(q)
	q.getElementsByClassName("code_run").item(0).addEventListener("click",()=>{
	    let cdo=q.getElementsByClassName("code_out").item(0);
	    cdo.innerHTML='';
	    Sk.configure({output:out(q),read:builtinRead});
	    let cde=q.getElementsByClassName("code_in").item(0);
	    let cdsrc=cde.tagName==="DIV"?cde.innerHTML:cde.value;
	    try{
		Sk.importMainWithBody("<stdin>",false,cdsrc);
	    }catch(aaa){
		q.getElementsByClassName("code_out").item(0).innerHTML=aaa;
	    }
	    if(cdo.innerHTML==='')cdo.innerHTML='<br>';
	});
	let b=q.getElementsByClassName("code_delete")
	if(b.length>0)
	    b.item(0).addEventListener("click",()=>{
		q.parentNode.removeChild(q);
	    });
    };
    var mk_py_eventify=(e,daddy=document.getElementById("code_edits"))=>{
	e.addEventListener("click",()=>{
	    let ok=document.createElement('div');
	    ok.setAttribute("class",'py_snip');
	    ok.innerHTML=document.getElementById("py_snip_edit_source").innerHTML;
	    daddy.appendChild(ok);
	    py_eventify(ok);
	});
    };
    var py_snips=document.getElementsByClassName("py_snip");
    for(var i=0;i<py_snips.length;i++){
	py_eventify(py_snips.item(i));	
    }
    var mk_py_snips=document.getElementsByClassName("new_py_snip");
    for(var i=0;i<mk_py_snips.length;i++){
	mk_py_eventify(mk_py_snips.item(i));
    }
    var builtinRead=(x)=>{
	if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
	    throw "File not found: '" + x + "'";
	return Sk.builtinFiles["files"][x];
    };
    var stringify_snip=(e)=>{
	let title=e.getElementsByClassName("code_title_inp").item(0);
	let cde=e.getElementsByClassName("code_in").item(0);
	let lang=e.getElementsByClassName("code_type").item(0);
	return "{%{{{{"+lang.innerHTML.toLowerCase()+"\n"+title.value+"\n"+cde.value+"}}}}%}"
    };
    var snippify_string=(s,daddy)=>{
	var r=s.indexOf("{%{{{{")
	var r1=s.indexOf("\n",r);
	var r2=s.indexOf("\n",r1+1);
	var nd=s.indexOf("}}}}%}",r2);
	if(r==-1||r1==-1||r2==-1||nd==-1)return;
	var lang=s.substring(r+6,r1);
	var title=s.substring(r1+1,r2);
	var body=s.substring(r2+1,nd);
	if(lang=="py"){
	    let ok=document.createElement('div');
	    ok.setAttribute("class","py_snip");
	    ok.innerHTML=document.getElementById("py_snip_source").innerHTML;
	    ok.getElementsByClassName("code_title_inp").item(0).innerHTML=title==""?lang+" code snippet":title;
	    ok.getElementsByClassName("code_in").item(0).innerHTML=body;
	    py_eventify(ok);
	    daddy.appendChild(ok);
	}
    }
    document.getElementById("stringify_test").addEventListener("click",()=>{
	snippify_string(stringify_snip(document.getElementsByClassName("py_snip").item(0)),document.getElementById("code_edits"));
    });
});
