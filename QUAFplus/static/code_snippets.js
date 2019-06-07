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
			ok.setAttribute("class",'py_snip col-lg-4 col-md-6 col-sm-12');
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
		return "{%{{{{"+lang.innerHTML.toLowerCase().replace("\n","").replace("\r","")+"\n"+title.value.replace("\n","").replace("\r","")+"\n"+cde.value.replace("\n","").replace("\r","")+"}}}}%}"
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
			ok.setAttribute("class","py_snip col-lg-4 col-md-8 col-sm-12");
			ok.innerHTML=document.getElementById("py_snip_source").innerHTML;
			ok.getElementsByClassName("code_title_inp").item(0).innerHTML=title==""?lang+" code snippet":title;
			ok.getElementsByClassName("code_in").item(0).innerHTML=body;
			py_eventify(ok);
			daddy.appendChild(ok);
		}
    }
	var post=(path,params)=>{
		const form = document.createElement('form');
		form.method = 'post';
		form.action = path;
		for (const key in params) {
			if (params.hasOwnProperty(key)) {
				const hiddenField = document.createElement('input');
				hiddenField.type = 'hidden';
				hiddenField.name = key;
				hiddenField.value = params[key];
				form.appendChild(hiddenField);
			}
		}
		document.body.appendChild(form);
		form.submit();
	}
	var mkpost=()=>{
		console.log("submitting");
		var title=document.getElementById("new_post_title").value;
		var body=document.getElementById("new_post_body").value;
		var snips="";
		var ok=document.getElementById("code_edits").children;
		var parent=document.getElementById("parent").innerHTML;
		var server=document.getElementById("server").innerHTML;
		for(var i=0;i<ok.length;i++){
			snips+=stringify_snip(ok.item(0));
		}
		post("/make_post",{"title":title,"body":body,"snips":snips,"parent":parent,"server":server})
	}
	mkpstbtn=document.getElementById("make_post")
	if(mkpstbtn){
		mkpstbtn.addEventListener("click",mkpost);
	}
    
	var tree={'id':3,'title':"test",'body':"body","snips":'{%{{{{py\npy\nprint("hello")}}}}%}','author':{'first':"THEODORE",'last':"PETERS",'uid':1},'parent':-1,'tags':[],'date':"daymonthyear",'server':8,'answered':false,'best':0,'question':true,'children':[{'id':4,'title':"test",'body':"body","snips":'{%{{{{py\npy\nprint("hello")}}}}%}','author':{'first':"THEODORE",'last':"PETERS",'uid':1},'parent':-1,'tags':[],'date':"daymonthyear",'server':8,'answered':false,'best':0,'question':true,'children':[]},{'id':5,'title':"test",'body':"body","snips":'{%{{{{py\npy\nprint("hello")}}}}%}','author':{'first':"THEODORE",'last':"PETERS",'uid':1},'parent':-1,'tags':[],'date':"daymonthyear",'server':8,'answered':false,'best':0,'question':true,'children':[]}]}

	var postify=(top,daddy)=>{
		console.log(top)
		let ok=document.createElement('div');
		ok.setAttribute("class","post");
		ok.innerHTML=document.getElementById("post_template").innerHTML;
		ok.getElementsByClassName("post_title").item(0).innerHTML=top['title']
		ok.getElementsByClassName("post_author").item(0).innerHTML=top['author']['first']+' '+top['author']['last']
		ok.getElementsByClassName("post_date").item(0).innerHTML=top['date']
		ok.getElementsByClassName("post_body").item(0).innerHTML=top['body']

		btn=ok.getElementsByClassName("post_collapse_head").item(0);
		btni="post_heading_"+top['id'];
		chl=ok.getElementsByClassName("post_collapse_body").item(0);
		chli="post_collapse_"+top['id'];
		acc=ok.getElementsByClassName("post_collapse_accordion").item(0);
		acci="post_accordion_"+top['id'];

		acc.setAttribute("id",acci);
		btn.setAttribute("id",btni);
		btn.setAttribute("data-target","#"+chli);
		btn.setAttribute("data-parent","#"+acci);
		btn.setAttribute("aria-controls",chli);
		chl.setAttribute("id",chli);
		chl.setAttribute("aria-labeledby",btni);
		
		snippify_string(top['snips'],ok.getElementsByClassName("post_code_snippets").item(0))
		for(var mid in top['children']){
			
			postify(top['children'][mid], ok.getElementsByClassName("post_children").item(0));
		}
		console.log(ok)
		daddy.appendChild(ok);
	};

	postify(tree,document.getElementById("post_base"));
});
