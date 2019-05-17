document.addEventListener("DOMContentLoaded",()=>{
    var out=(e)=>{
	return(t)=>{
	e.getElementsByClassName("code_out")[0].innerHTML=t;
	};
    };

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
