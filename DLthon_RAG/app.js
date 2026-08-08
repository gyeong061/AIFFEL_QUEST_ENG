const styleImage =
    document.getElementById("styleImage");


const preview =
    document.getElementById("preview");


const button =
    document.getElementById("generateBtn");


const prompt =
    document.getElementById("prompt");


const comicGrid =
    document.getElementById("comicGrid");


const loading =
    document.getElementById("loading");



// 이미지 미리보기

styleImage.addEventListener(
    "change",
    function(e){

        const file = e.target.files[0];

        if(file){

            preview.src =
                URL.createObjectURL(file);

            preview.style.display =
                "block";

        }

    }
);



// 생성 버튼

button.addEventListener(
    "click",
    async function(){


        if(!prompt.value){

            alert(
                "만화 내용을 입력해주세요."
            );

            return;

        }


        loading.style.display =
            "block";


        comicGrid.innerHTML="";


        /*
            실제 연결 위치

            여기에서 백엔드 API 호출

            예:

            const response =
                await fetch(
                  "http://localhost:8000/generate",
                  {
                    method:"POST",
                    body:data
                  }
                )

        */


        await fakeGenerate();



        loading.style.display =
            "none";


    }

);




// 데모 생성 함수

function fakeGenerate(){


    return new Promise(
        resolve=>{


            setTimeout(()=>{


                const images=[

                    "https://placehold.co/600x600?text=Panel+1",

                    "https://placehold.co/600x600?text=Panel+2",

                    "https://placehold.co/600x600?text=Panel+3",

                    "https://placehold.co/600x600?text=Panel+4"

                ];


                images.forEach(
                    (img,index)=>{


                        const div =
                            document.createElement(
                                "div"
                            );


                        div.className =
                            "panel";


                        div.innerHTML =
                        `
                        <img src="${img}">
                        `;


                        comicGrid.appendChild(div);


                    }
                );


                resolve();


            },2000);

        }
    )

}