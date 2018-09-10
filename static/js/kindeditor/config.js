KindEditor.ready(function (K) {
    K.create('textarea[name=article]',{
        width: '800px',
        height: '400px',
        uploadJson: '/admin/load/kindeditor'  /*该路径名要与uploads下的kindeditor对应*/
    });
});