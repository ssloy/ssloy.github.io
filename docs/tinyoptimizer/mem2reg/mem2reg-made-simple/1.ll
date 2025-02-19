define i32 @mem2reg_made_simple() {
entry:
	%a = alloca i32
	br label %bb1
bb1:
	store i32 1, ptr %a
	br i1 1, label %bb2, label %bb4
bb2:
	%a0 = load i32, ptr %a
	%t0 = add i32 %a0, 1
	store i32 %t0, ptr %a
	br label %bb3
bb3:
	%a1 = load i32, ptr %a
	%t1 = add i32 %a1, %a1
	store i32 %t1, ptr %a
	br i1 1, label %bb8, label %bb2
bb5:
	%a2 = load i32, ptr %a
	store i32 2, ptr %a
	br label %bb7
bb4:
	br i1 1, label %bb5, label %bb6
bb6:
	%a3 = load i32, ptr %a
	store i32 3, ptr %a
	br label %bb7
bb7:
	%a4 = load i32, ptr %a
	br label %bb8
bb8:
	%a5 = load i32, ptr %a
	ret i32 %a5
}

