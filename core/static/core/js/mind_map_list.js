
function mindMap(markdown, id) {
  const { markmap } = window;
  const { Transformer, Markmap, loadCSS, loadJS } = markmap;
  const transformer = new Transformer();

  const { root } = transformer.transform(markdown);

  Markmap.create(id, { autoFit: true }, root);
}



function viewMindMaps(){
  const mindMaps = document.getElementsByTagName('svg')

  for (const item of mindMaps){
    mindMap(item.dataset.markdown, `#${item.id}`)
  }
}

viewMindMaps()