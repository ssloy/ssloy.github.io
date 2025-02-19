define i32 @mem2reg_made_simple() {
entry:
	br label %bb1
bb1:
	br i1 1, label %bb2, label %bb4
bb2:
	%a_bb2 = phi i32 [1, %bb1], [%t1, %bb3]
	%t0 = add i32 %a_bb2, 1
	br label %bb3
bb3:
	%t1 = add i32 %t0, %t0
	br i1 1, label %bb8, label %bb2
bb5:
	br label %bb7
bb4:
	br i1 1, label %bb5, label %bb6
bb6:
	br label %bb7
bb7:
	%a_bb7 = phi i32 [2, %bb5], [3, %bb6]
	br label %bb8
bb8:
	%a_bb8 = phi i32 [%t1, %bb3], [%a_bb7, %bb7]
	ret i32 %a_bb8
}

