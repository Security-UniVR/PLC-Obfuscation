  VAR
     obf_r: INT := 100;
   END_VAR
  VAR
   	${new_var} AT %${new_reg}: BOOL;
  END_VAR
  VAR
    obf_ra : BOOL;
  END_VAR
  VAR
    rand_generator0 : rand_generator;
  END_VAR

  rand_generator0(IN := ${dep_register});
  obf_ra := LE(rand_generator0.OUT, obf_r);
  ${new_var} := NOT(${new_var}) AND obf_ra;

