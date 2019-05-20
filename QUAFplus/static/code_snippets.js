document.addEventListener("DOMContentLoaded",()=>{
    var out=(e)=>{
		return(t)=>{
			e.getElementsByClassName("code_out").item(0).innerHTML+=t;
		};
    };
	py_snips=document.getElementsByClassName("py_snip");
	for(var  i=0;i<py_snips.length;i++){
		let q=py_snips.item(i);
		console.log(q);
		q.getElementsByClassName("code_run").item(0).addEventListener("click",()=>{
			q.getElementsByClassName("code_out").item(0).innerHTML='';
			Sk.configure({output:out(q),read:builtinRead});
			try{
				Sk.importMainWithBody("<stdin>",false,q.getElementsByClassName("code_in").item(0).value);
			}catch(aaa){
				q.getElementsByClassName("code_out").item(0).innerHTML=aaa;
			}
		});
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
