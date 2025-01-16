add_executable(sdr2file sdr2file.cpp)
target_link_libraries(
  soapy_example
  PRIVATE gr-basic
          gr-fileio
          gr-testing
          gr-soapy
          ut)
