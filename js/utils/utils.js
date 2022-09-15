public static void main(String[] args) {
    folderInFiles("F:\\eclipse\\workspace");
  }
  
  public static void folderInFiles(String path) {
    File folder = new File(path);
    File files[] = folder.listFiles();
  
    for(int i=0; i<files.length; i++) {
      File file = files[i];
      if(file.isDirectory()) {
        folderInFiles(file.getPath());
      } else {
        System.out.println(files[i]);
      }
    }
  }