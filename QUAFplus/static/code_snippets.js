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
    var mk_py_eventify=(e,daddy=document.getElementById("container"))=>{
	let ok=document.createElement('div');
	ok.setAttribute("class",'py_snip');
	ok.innerHTML=document.getElementById("py_snip_edit_source").innerHTML;
	daddy.appendChild(ok);
    }
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
    }
    /*
    var runit=()=>{
	var prog = document.getElementById("yourcode").value;
	var mypre = document.getElementById("output");
	mypre.innerHTML = '';
	Sk.configure({output:outf,read:builtinRead});
	try {
	    Sk.importMainWithBody("<stdin>",false,prog);
	} catch(e) {
	    alert(e);
	}
    }
    */
});
