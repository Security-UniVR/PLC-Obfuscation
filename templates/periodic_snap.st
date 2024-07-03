  VAR
    current_time_internal AT %ML1024 : ULINT;
  END_VAR
  VAR
    obf_p: INT := ${period};
    obf_tmp: INT;
	obf_t: INT;
  END_VAR
  VAR
 	${new_var} AT %${new_reg}: BOOL;
  END_VAR
  
  obf_t := ABS(LWORD_TO_INT( AND( LINT_TO_LWORD(2147483647), ULINT_TO_LWORD(current_time_internal) ) ));
  obf_tmp := MOD(obf_t, obf_p);
  ${new_var} := LE(obf_tmp, DIV(obf_p,2));


