setlocal
set MG4J=D:\git\mg4j-workbench
set BITFUNNEL=D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe
set GOV2=d:\data\gov2

for /d %%i in (%GOV2%\GX000.7z %GOV2%\GX001.7z) do (
  mkdir d:\data\work\temp
  mkdir d:\data\work\chunks

  pushd d:\data\work\temp
  7z x %%i
  popd

  echo Create collection d:\data\work\temp\%%~ni.collection

  dir /s/b d:\data\work\temp\%%~ni\*.txt | java -cp %MG4J%\target\mg4j-1.0-SNAPSHOT-jar-with-dependencies.jar ^
     it.unimi.di.big.mg4j.document.TRECDocumentCollection ^
     -f HtmlDocumentFactory -p encoding=iso-8859-1 d:\data\work\temp\%%~ni.collection


  echo Create chunk d:\data\work\temp\%%~ni.chunk
  java -cp %MG4J%\target\mg4j-1.0-SNAPSHOT-jar-with-dependencies.jar ^
       org.bitfunnel.reproducibility.GenerateBitFunnelChunks ^
       -S d:\data\work\temp\%%~ni.collection d:\data\work\temp\%%~ni.chunk

  echo Create manifest file
  dir /s/b d:\data\work\temp\%%~ni.chunk > d:\data\work\temp\manifest.txt

  echo Create filtered chunk d:\data\work\chunks\%%~ni-100-150.chunk
  %BITFUNNEL% filter ^
      d:\data\work\temp\manifest.txt d:\data\work\chunks -size 100 150

  ren d:\data\work\chunks\Chunk-0.chunk %%~ni-100-150.chunk

  echo Cleanup
  rmdir /s d:\data\work\temp
)

endlocal

